# RC-15: base typing of the W&H2 loads at +0x64..+0x83 (static reader for FABLE, 2026-09-29)

**Question.** Of the 43 functions in `t6_regfile_loads_h2.out` (W & H2), does any native load other than the
interpreter's read the script VM register file of an ActorStorageRecord? The register file is I0..I3 (dwords at
+0x64/+0x68/+0x6C/+0x70) and F0..F3 (floats at +0x74/+0x78/+0x7C/+0x80).

**Method.** Each base register was traced in the disassembly (`disr.py`; `rawdis.py` in this folder for the unlisted
tail-jump at `002E5B5A`). Argument bases were followed to every raw caller's actual argument (`tools/rawcalls.py`), and
globals to their writers (`tools/ripscan.py`). The linear slices in `t6_basedefs_h2.out` were used only as hints. Three of
them are wrong:
- `002ED6A0`: `rdx` is the second argument, not the result of `0026E530`.
- `003A4290`: `rbp` is the frame pointer, not an entry value.
- `00262440`/`0026D3E0`/`00265770`: `rcx` is the actor **manager**, not an unknown entry value.

**Reference points.**
- **Manager:** `02098E10 + i*0x288`. Its `+0x00` is the loaded script image (the header), and `+0x08` is the record pool.
  `ActorManager_GetRecordByOrdinal` `00358940` reads `[rcx+8]`, so its `rcx` is a manager.
- **Interpreter:** `WorldActorScriptVM_InterpretBytecode` `0025E4C0` takes the manager in `rcx`, kept in `r13`
  (`0025E4DF`), and the record in `rdx`, kept in `r15` (`0025E4D5`). Its caller `0025DF00` passes `rcx = r15 = its own rcx`
  (`0025DF32`, `0025E0D0`). That comes from `ActorManager_RunFieldRuntimePass`, which passes `rcx = rbx`, and `rbx` is
  `02098E10 + i*0x288` (`0025D9EF`-`0025D9FD`, `0025DB3D`). Its `rdx` is `00358940`'s result (`0025DB35`-`0025DB3A`).

## Rows

Verdict key: **no** = the base is not an ActorStorageRecord, or the access cannot be a register read.

### Functions typed in this pass

| function | load(s) | base type | width / use | evidence | verdict |
|---|---|---|---|---|---|
| `0025E4C0` interpreter (the **control**) | `002616AF`..`0026172C` `[r15+0x64..0x80]` | **ActorStorageRecord** (`r15` = `rdx` arg = `00358940` result) | dword I0..I3 → `VMValueStack_PushInt32`; float F0..F3 → `VMValueStack_PushFloat32Bits` | `0025E4D5`, `0025DB35`-`0025DB43` | **yes (control)** |
| `0025E4C0` (the other loads) | `002617C9`/`00261806` `[r13+0x80]`, `00261855` `[r13+0x68]`, `0026187D` `[r13+0x70]` | actor **manager** (`r13` = `rcx` arg) | qword table pointers (`+0x68` int constants, `+0x70` float constants, `+0x80` table), then indexed | `0025E4DF`, `0025DF32`/`0025E0D0`, `0025D9F6`-`0025D9FD` | no |
| `00262440` (the variable resolver) | `00262459` `[rcx+0x78]`, `002625CD`/`0026262D` `[rdi+0x60]` | actor **manager**: `rcx`/`rdi` is the interpreter's `r13`. All four callers pass it: `002617A5` directly, and POPV `00267E60`, PUSHV `00267FC0` and `00268100` pass their own `rcx` through, each called from the interpreter with `rcx = r13` (`0026176B`, `00261782`, `002617BC`). The record comes in `rdx` (`rbp`) and is used only as the class-2 callback argument (`002625A5`) | qword region pointers (`+0x78` the variable table, `+0x60` the class-5 region) | `00262471`, `002617A5`, `00267E7F`, `00267FD9`, `00268113` | no |
| `00265770` (the region selector) | `002657AD` `[r9+0x60]` | actor **manager**: its only caller `002641B0` passes `rcx = rdi = 02098E10 + ecx*0x288` (`002641BD`-`002641CE`, `0026421E`) | qword; the same class switch as `00262440` (`+0x48`/`+0x40`/`+0x98` callback/`+0x58`/`+0x60`) | `00264221` | no |
| `0026D3E0` (the initial-value copy at manager init) | `0026D3EA` `[rcx+0x78]`, `0026D4AC` `[r14+0x60]` | actor **manager**: `r14` is passed as `rcx` to `00358940` (`0026D45C`-`0026D45F`); only caller `ActorSystem_InitializeManagerRuntime` (`0026D300`) | qword region pointers. Class 2 goes through the callback `[r14+0x98]`, which is `00264E30` = `[slot+0x50] + [[record+0x40]+0x1C]`, a pointer **into the image**, not the record (installed `0026CB6F`-`0026CB76`) | `0026D3EE`, `0026D45F`, `00264E30`-`00264E3C` | no |
| `002641B0` | `002641E4`/`002641F1` `[rbx+0x6c]` | **script image header**: `rbx = [rdi]`, where `rdi` = manager `02098E10 + ecx*0x288` (`002641BA`-`002641DC`) | dword **offset**, passed to `ImageAddress_ResolveRuntimePointer` and added back to the header (`002641E7`, `002641FC`) | `002641DC` | no |
| `00264B90` | `00264BFF` `word [rbx+0x78]`, `00264C0A` `word [rbx+0x7a]` | **script image header**: `rbx = [02098E10 + edx*0x288]` (`00264BC7`-`00264BDC`) | **word** (`movsx`) index defaults | `00264BDC` | no |
| `00264770` | `00264785` `word [rax+0x7e]` | **script image header** of manager 0: the cell `02098E10` (manager 0 `+0x00`), gated on manager 0's `+0x10` bit 0 (`02098E20`) | **word** | `00264770`, `00264779` | no |
| `00264790` | `002647A5` `word [rax+0x7c]` | **script image header** of manager 0 (cell `02098E10`) | **word** | `00264799` | no |
| `00264AE0` | `00264B03`/`00264B10` `[rbx+0x70]` | **script image header** of manager 0 (cell `02098E10`) | dword offset → `ImageAddress_ResolveRuntimePointer`, added to the header (`00264B1B`) | `00264AF7` | no |
| `002658B0` | `002658EB` `[rdi+0x64]` | **script image header** of manager 0 (cell `02098E10`); checks the header's version word `>= 7` first (`002658E5`) | dword offset → `ImageAddress_ResolveRuntimePointer`, added to the header (`002658FA`) | `002658D9` | no |
| `0035A270` | `0035A2A0` `[rbx+0x80]` | **script image header**: `rbx = [00263FF0(ecx)]`, and `00263FF0` returns `02098E10 + ecx*0x288` (`00263FF0`-`00264004`) | dword offset → `ImageAddress_ResolveRuntimePointer`, added to the header (`0035A2BB`-`0035A2BF`) | `0035A284`, `0035A294` | no |
| `0035AB50` | `0035AB80` `[rbx+0x80]` | **script image header** (the same shape as `0035A270`) | dword offset → `ImageAddress_ResolveRuntimePointer` | `0035AB64`, `0035AB74` | no |
| `003B7210` | `003B7226` `[rbx+0x68]` | **script image header** of manager 3: `rbx = [rcx]`, and `rcx` (`r14`) is passed to `00358940` (`003B7292`-`003B7295`). Its only caller `00348A70` tail-jumps with `rcx = 00263FF0(3)` (`00348A74`-`00348A85`) | dword offset → `ImageAddress_ResolveRuntimePointer` | `003B7220` | no |
| `003B72F0` | `003B730E` `[rdi+0x68]` | **script image header** of manager 3 (the same shape): `rdi = [rcx]`, `r14` → `00358940` (`003B7366`). Its only caller `00348130` passes `00263FF0(3)` (`00348136`-`00348150`) | dword offset → `ImageAddress_ResolveRuntimePointer` | `003B7300` | no |
| `0035B4B0` | `0035B4F8` `byte [rax+0x7b]` | **static table** at `02EC0B81`, stride 0x20 and walked in 0x80 steps up to `02EC0F81`; `+0x7b` is element 3's `+0x1b` | **byte** bit test against the argument mask | `0035B4C0`, `0035B501`-`0035B508` | no |
| `0035BB70` | `0035BBAA` `[rcx+0x7c]`, `0035BBE1` `byte [rbx+0x7c]`, `0035BBF8` `[rbx+0x7c]` | **widgets** held in the cells `022CA428` and `022CA430`. Their handlers store `self` there on create: `0035D6B0` stores `rbx` at `0035D869`, and `0035E070` stores `r15` at `0035E146`. Those handlers are registered through the widget factory `00244F50` (`0035D0B5`/`0035D0C1` size 0xC8; `0035DFC5`/`0035DFCC` size 0x6E8) | the dword is a **flag word**: tested for bit 5 (0x20), then masked with `and 0x3ff7ff` / `or 0x400800` and written back (`0035BBB8`-`0035BBC2`), followed by the widget-close `00244F00` | `0035BB9E`, `0035BBD5`, `0035D869`, `0035E146` | no |
| `002A2720` | `002A2755` `byte [rbx+0x7c]` | **widget** (`rbx` = `rcx` arg). Callers pass the widget root `[0208EA28]` (`0035D0FB`/`0035D123`, `0035D148`/`0035D16A`), its child chain `[w+0x18]` (`0035D280` ← `0035D12B`), or the widget in slot `+0` of the 8 × 0x68 table `0215F200` (`002E0725`, `002E07F1`, `002E08E7`, `002E183E`). The body checks the widget registry `0209C4D0[byte +0x3B8]` and the flag word `+0x40` | **byte** bit test (0x20), the same flag word as `0035BB70` | `002A2738`, `002A2742`, `002A274C` | no |
| `002ED6A0` | `002ED6D5` `[rdx+0x64]`, `002ED6DB` `[rdx+0x68]`, `002ED6E1` `[rdx+0x6c]` (with `002ED6CF` `[rdx+0x60]`) | **second argument** (the slice's "call result" is wrong). Both callers pass `rdx = [[owner+0xC0]+0x138]`, a pointer taken from the owner's `+0xC0` sub-object: `002E4AED` in `002E4A40`, and the unlisted `002E5B16` before `jmp 002ED6A0` at `002E5B5A` | a **16-byte block copy** `+0x60..+0x6F → +0x50..+0x5F`. `+0x60` is not a register slot. The unlisted sibling writes the same object as two float4s, `+0x50..+0x5C` and `+0x60..+0x6C` (`002E5B31`-`002E5B54`) | `002ED6AA`, `002E4AED`, `002E5B16` | no |
| `0030A6E0` | `0030A71F` `[rax+0x64]` | **battle-stats slot**: `BattleStats_GetByBattleSlotIndex` `00320A40` returns `[02EBF190] + 8 + idx*0x1C8` | dword ORed with `+0x3C` and tested for `0x80000003`: a status mask | `0030A712`, `00320A4B`-`00320A5D` | no |
| `00329A80` | `00329AB4` `[rax+0x64]`, `00329ACB` `[rbx+0x70]` | `rax` = battle unit `+0x698` (the battle-stats link); `rbx` = **battle unit** = `ActorWork_GetBattleUnitRaw` `00263E30` = `[record+0x30]` | `+0x64` is the status mask (`or [+0x3c]`, `test 0x80000003`); `+0x70` is a float read-modify-write on the battle unit (`00329AD0`) | `00329A96`, `00329AA8`, `00263E30` | no |
| `003266C0` (`00326B74`) | `00326B74` `[rdx+0x64]` | **battle-stats slot**, the `00320A40` computation inlined: `[02EBF190] + 8 + al*0x1C8` (`00326B52`-`00326B6F`). The row's other load, `00326ABA`, goes through `+0x698` | status mask (`or [+0x3c]`, `test 0x80000003`) | `00326B64`-`00326B6F` | no |
| `003A4290` | `003A4EC8`..`003A5003` floats `[rbp+0x64..0x74]`, `003A550B` `[rbp+0x78]` | **stack frame**: `rbp = rsp_entry - 0xF8` (`003A429F`). `rbp+0x60..+0x77` is a local six-float box filled by `003E5130`/`003E5070` through `lea rdx,[rbp+0x60]` (`003A4E8D`, `003A4EBF`) and written back at `003A501B`-`003A505C`. `rbp+0x78` is the GS cookie (`003A42C4`, `003A550B`-`003A5512`) | a local min/max box, and the cookie | `003A429F`, `003A42C4` | no |
| `003E5B30` | `003E5B72` `qword [rax+0x70]` | a 0xA0-stride element found by `0041C970` inside the entry `CharacterRenderRecord_ResolveActivePresentationEntry` `00422D50` returns (`0041C975`-`0041C98C`) | **qword** pointer | `003E5B4D`, `003E5B68` | no |
| `00375900` | `00375931` `[rax+0x70]`, `003759F7` `qword [rbx+0x60]`, `00375A0E` `[rcx+0x68]` | `rax` walks the **static table** `02EBF9E0` (32 × 0x70). `rax` starts at `02EBFAB8`, which is entry 1's `+0x68`, so `[rax+0x70]` is the next entry's `+0x68` in-use serial (`00375916`, `00375940`). `rcx` = `02EBF9E0 + idx*0x70` (`00375995`-`003759A0`), reading back the serial written at `003759BB`. `rbx` = `rcx` arg, a 0x68-byte request descriptor. Every one of the 47 raw call sites passes a stack local (`lea rcx,[rsp/rbp±…]`), the static slot `022BDD60 + i*0x30 + 8` (`002EFAA3`-`002EFAB8`, `002EFCC5`), or `02B58A80 + i*0x68 + 0x10` (`003DDFC4`-`003DDFF7`) | a dword serial; the `+0x60` qword is the tail of a 0x68-byte `movups`/`movsd` blob copy (`003759C9`-`00375A01`) | `0037590F`, `00375995`, `002EFCC5`, `003DDFF7` | no |

### Functions typed before this pass (listed for completeness; the slice lines are in `t6_basedefs_h2.out`)

| function | load(s) | base type | verdict |
|---|---|---|---|
| `00233D70`, `00233EA0`, `00234200`, `00234D40`, `00237F40`, `0030BFB0`, `0032A060`, `003266C0` (`00326ABA`) | dword `+0x64` | battle unit `+0x698` link → battle-stats slot (status mask, as at `00326ABA`-`00326AC0`) | no |
| `00239960` | byte `+0x6c`, byte `+0x7c` | `00320A40` result (battle-stats slot), `00239BD2` | no |
| `00259620` | vec4 `+0x60`/`+0x70`/`+0x80` | stack (`lea rax,[rsp+0x20]`, `00259721`) | no |
| `0025B070` | dword `+0x74` | `[x+0xB8]` sub-object (`0025B0D7`, `0025B16C`) | no |
| `0025BE50`, `0025C830`, `00268380` | float `+0x68`/`+0x6c` | `[x+0xB8]` sub-object (`0025BE63`, `0025C85A`, `0026841F`) | no |
| `0025DF00` | float `+0x7c` | `[[record+0xB8]+0xF0]` (`0025DF49`-`0025DF50`) | no |
| `00265B60` | byte `+0x70`/`+0x71` | `[x+0xC0]` sub-object (`00265C34`) | no |
| `002693D0`, `0026C120`, `002EBE50`, `002EC3F0` | byte/word/dword/float | `[x+0xF0]` sub-object (`0026945B`, `0026C1A7`/`0026C244`, `002EBEBC`/`002EBED5`/`002EBEF7`, `002EC408`) | no |

That covers all 43 functions: 24 in the first table (the interpreter counted once) and 19 more here (`003266C0` is in both).

## Conclusion

**No native code other than the interpreter reads the register file (within the H2 reach set).**

Every other load at +0x64..+0x83 in W & H2 has one of these bases:
- the actor **manager** (`02098E10 + i*0x288`);
- the manager's **script image header** (`[manager+0]`), whose +0x64..+0x80 dwords are image offsets for
  `ImageAddress_ResolveRuntimePointer` and whose +0x78..+0x7E are word indices;
- a **widget** (from the `00244F50` factory) with a flag word at +0x7C;
- a **battle-stats slot**, the **battle unit**, or the record's **+0xB8/+0xC0/+0xF0 sub-objects**;
- a **static table**, or a **stack frame**.

Only the control `002616AF`..`0026172C` reads `[record+0x64..0x80]`.

**Unresolved rows: none.**

Scope notes:
- This types displacement loads only. The VM's indexed variable accesses (`00262440` → `0026D530` store, PUSHV load) do
  not reach the record either: the `local` class resolves through `00264E30` into the script image
  (`[slot+0x50] + [[record+0x40]+0x1C]`), and the other classes use manager/image regions.
- `0026D3E0`'s `memcpy` (`0026D4D5`) is a store, not a load. Its class-2 destination is that same image pointer, so it
  does not write the record either.
