# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-element-types-40-42-a0-ab-d0-d1.json`.

Functions: 17. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 65f4854dd	SWE2-STRUCT pass-22 debt + OV31 narrowing: 77 crossing bullets across 21 docs (5 lane folders now re; c97af7156	SWE2-FRONTIER: owner re-status - the 13 GI pages move PARTIAL -> DOCUMENTED (GI-1..GI-13 answered an; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 00182830 (64 B, extent 00182830-00182870)

Page context: "lls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes | | '0xA2' | step '00462480' (177 B, '003D8E50'-family), walk '00462540' 2921 B |"

```
00182830  sub      rsp, 0x48
00182834  movaps   xmmword ptr [rsp + 0x30], xmm6
00182839  movaps   xmm6, xmm1
0018283C  movaps   xmmword ptr [rsp + 0x20], xmm7
00182841  movaps   xmm7, xmm0
00182844  call     0x193d50  ; -> 00193D50 fn
00182849  test     rax, rax
0018284C  je       0x182861  ; -> 00182861
0018284E  call     0x193d50  ; -> 00193D50 fn
00182853  mov      rcx, rax
00182856  movaps   xmm2, xmm6
00182859  movaps   xmm1, xmm7
0018285C  call     0x194470  ; -> 00194470 fn
00182861  movaps   xmm6, xmmword ptr [rsp + 0x30]
00182866  movaps   xmm7, xmmword ptr [rsp + 0x20]
0018286B  add      rsp, 0x48
0018286F  ret      
```

## 00327270 (36 B, extent 00327270-00327294)

Page context: "mmand_SetSecondaryFocusActorFromActorIndex', 'PartyFocus_SelectAndRequestDefaultActor', 'PartyRoster_AssignActorAndCommitFocusWhenEligible' share '003589B0'; 'PartyFocus_IsCurrentPackedActorHandle', '00327270', 'BattleUnit_GetPartyLeader', '003272F0', 'PartyRoster_GetActorBySlotOrCurrentFocus' share '003590D0'; '00465120' calls 'PartyFocus_GetCurrentPackedActorHandle'. Shared accessor fan-in.  **Audio — MECHANICAL (SWE2-CONTRACT 2026-09"

```
00327270  sub      rsp, 0x28
00327274  call     0x3590d0  ; -> 003590D0 fn
00327279  test     byte ptr [rip + 0x1d620c0], 0x10  ; -> 02089340
00327280  je       0x32728d  ; -> 0032728D
00327282  mov      ecx, eax
00327284  add      rsp, 0x28
00327288  jmp      0x3588b0  ; -> 003588B0 fn
0032728D  xor      eax, eax
0032728F  add      rsp, 0x28
00327293  ret      
```

## 00345430 (233 B, extent 00345430-00345519)

Page context: "FA0'/'Movement_IntegratePositionAndMeasureDisplacement' share '003589B0'; ten movement bodies ('Movement_UpdateSteeringTowardTarget', 'BattleUnit_CanAdvanceCombatNavigation', '0026C3E0', '0026D810', '00345430', '00319490', '002E5180', '00326BB0', …) share '003590D0'; '001EDDA0' is shared with 'WorldActor_UpdateRuntimeAndScriptExecutionState'.  **Party — MECHANICAL (SWE2-CONTRACT 2026-09-15, 12 edges).** 'PartyRoster_AssignActorToSlot' s"

```
00345430  mov      qword ptr [rsp + 0x18], rbp
00345435  push     rsi
00345436  push     r14
00345438  push     r15
0034543A  sub      rsp, 0x20
0034543E  mov      rsi, r9
00345441  mov      r14, r8
00345444  mov      r15, rcx
00345447  call     0x3590d0  ; -> 003590D0 fn
0034544C  mov      ecx, eax
0034544E  call     0x3588b0  ; -> 003588B0 fn
00345453  mov      rbp, rax
00345456  test     rax, rax
00345459  je       0x3454f3  ; -> 003454F3
0034545F  mov      qword ptr [rsp + 0x40], rbx
00345464  mov      rcx, rax
00345467  mov      qword ptr [rsp + 0x48], rdi
0034546C  call     0x264420  ; -> 00264420 fn
00345471  mov      rcx, rbp
00345474  mov      ebx, eax
00345476  call     0x30beb0  ; -> 0030BEB0 fn
0034547B  mov      edi, eax
0034547D  call     0x3590b0  ; -> 003590B0 fn
00345482  movaps   xmm1, xmm0
00345485  mov      rcx, rsi
00345488  call     0x267f60  ; -> 00267F60 fn
0034548D  mov      r8d, 2
00345493  mov      edx, ebx
00345495  mov      rcx, rbp
00345498  call     0x2ecf10  ; -> 002ECF10 fn
0034549D  mov      r9, rsi
003454A0  mov      r8, r14
003454A3  mov      rdx, rbp
003454A6  mov      rcx, r15
003454A9  call     0x357a20  ; -> 00357A20 fn
003454AE  mov      rcx, rbp
003454B1  call     0x263f40  ; -> 00263F40 fn
003454B6  mov      rcx, rax
003454B9  call     0x2eb430  ; -> 002EB430 fn
003454BE  mov      edx, 2
003454C3  mov      rcx, rbp
003454C6  call     0x26c120  ; -> 0026C120 fn
003454CB  mov      r8d, edi
003454CE  mov      edx, 1
003454D3  mov      rcx, rbp
003454D6  mov      rdi, qword ptr [rsp + 0x48]
003454DB  mov      rbx, qword ptr [rsp + 0x40]
003454E0  mov      rbp, qword ptr [rsp + 0x50]
003454E5  add      rsp, 0x20
003454E9  pop      r15
003454EB  pop      r14
003454ED  pop      rsi
003454EE  jmp      0x269d80  ; -> 00269D80 fn
003454F3  mov      rcx, rsi
003454F6  call     0x267db0  ; -> 00267DB0 fn
003454FB  mov      rcx, rsi
003454FE  call     0x267db0  ; -> 00267DB0 fn
00345503  mov      rcx, rsi
00345506  mov      rbp, qword ptr [rsp + 0x50]
0034550B  add      rsp, 0x20
0034550F  pop      r15
00345511  pop      r14
00345513  pop      rsi
00345514  jmp      0x267db0  ; -> 00267DB0 fn
```

## 00377360 (94 B, extent 00377360-003773BE)

Page context: "' on '+0x244'/'+0x24C'.~~ **Corrected 2026-09-29 (FABLE, GI-9):** two   different handles - it removes the light '+0x244' through '003ABCA0' and releases the registry slot '+0x24C' by   tail-jumping '00377360' ([what these types are](#what-these-seven-types-are-gi-9-2026-09-29-fable)). - '0x41': even smaller — update '00464F10' is a **5 B stub** (shared with '0xD0'),   walk '00464BC0' 8 B, setup '0053AB10' 52 B (base + '4G@+0x80' only; "

```
00377360  mov      rax, qword ptr [rip + 0x2764c61]  ; -> 02ADBFC8
00377367  test     rax, rax
0037736A  je       0x3773bd  ; -> 003773BD
0037736C  nop      dword ptr [rax]
00377370  cmp      dword ptr [rax], ecx
00377372  je       0x37737e  ; -> 0037737E
00377374  mov      rax, qword ptr [rax + 0x18]
00377378  test     rax, rax
0037737B  jne      0x377370  ; -> 00377370
0037737D  ret      
0037737E  dec      byte ptr [rip + 0x2764c3c]  ; -> 02ADBFC0
00377384  mov      rdx, qword ptr [rax + 0x10]
00377388  mov      rcx, qword ptr [rax + 0x18]
0037738C  mov      dword ptr [rax], 0
00377392  test     rdx, rdx
00377395  je       0x37739d  ; -> 0037739D
00377397  mov      qword ptr [rdx + 0x18], rcx
0037739B  jmp      0x3773a4  ; -> 003773A4
0037739D  mov      qword ptr [rip + 0x2764c24], rcx  ; -> 02ADBFC8
003773A4  mov      rdx, qword ptr [rax + 0x18]
003773A8  mov      rcx, qword ptr [rax + 0x10]
003773AC  test     rdx, rdx
003773AF  je       0x3773b6  ; -> 003773B6
003773B1  mov      qword ptr [rdx + 0x10], rcx
003773B5  ret      
003773B6  mov      qword ptr [rip + 0x2764c13], rcx  ; -> 02ADBFD0
003773BD  ret      
```

## 003B6F80 (254 B, extent 003B6F80-003B707E)

Page context: "rEntity neighbours ('ActorResource_FinalizeManagerRuntimeAfterLoads', 'ActorResource_AllocateAndSubmitEntry', 'ActorManager_RunFieldRuntimePass', 'ActorEntity.ManagerPopulationFiltering' '0046BAC0', '003B6F80', '0035A990', '0035A590', '0035A7A0', '003DB1F0', '00264010', '00268D10', '00264050', 'ActorHandle_ResolveRegistryEntryByPackedId', …) call the same six. Element steps resolve their host actor through the same accessors the whole e"

```
003B6F80  mov      qword ptr [rsp + 0x10], rbx
003B6F85  mov      qword ptr [rsp + 0x18], rbp
003B6F8A  mov      qword ptr [rsp + 0x20], rsi
003B6F8F  push     rdi
003B6F90  push     r12
003B6F92  push     r13
003B6F94  push     r14
003B6F96  push     r15
003B6F98  sub      rsp, 0xc0
003B6F9F  mov      rax, qword ptr [rip + 0x1b8d88a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003B6FA6  xor      rax, rsp
003B6FA9  mov      qword ptr [rsp + 0xb0], rax
003B6FB1  mov      r13, rcx
003B6FB4  call     0x3589b0  ; -> 003589B0 fn
003B6FB9  xor      r14d, r14d
003B6FBC  mov      dword ptr [rsp + 0x20], eax
003B6FC0  mov      r15d, r14d
003B6FC3  mov      esi, r14d
003B6FC6  mov      ecx, r15d
003B6FC9  call     0x263ff0  ; -> 00263FF0 fn
003B6FCE  mov      rbp, rax
003B6FD1  test     byte ptr [rax + 0x10], 1
003B6FD5  je       0x3b7033  ; -> 003B7033
003B6FD7  movzx    edi, word ptr [rax + 0x1de]
003B6FDE  movzx    r12d, word ptr [rax + 0x1d6]
003B6FE6  add      r12d, edi
003B6FE9  cmp      edi, r12d
003B6FEC  jae      0x3b7033  ; -> 003B7033
003B6FEE  nop      
003B6FF0  mov      edx, edi
003B6FF2  mov      rcx, rbp
003B6FF5  call     0x358940  ; -> 00358940 fn
003B6FFA  mov      rbx, rax
003B6FFD  test     byte ptr [rax + 9], 0x10
003B7001  je       0x3b7020  ; -> 003B7020
003B7003  cmp      r13, rax
003B7006  je       0x3b7020  ; -> 003B7020
003B7008  cmp      rsi, 0x1f
003B700C  jge      0x3b7020  ; -> 003B7020
003B700E  mov      rcx, rax
003B7011  call     0x3589b0  ; -> 003589B0 fn
003B7016  inc      r14d
003B7019  mov      dword ptr [rsp + rsi*4 + 0x30], eax
003B701D  inc      rsi
003B7020  and      byte ptr [rbx + 9], 0xeb
003B7024  mov      rcx, rbx
003B7027  call     0x26d6d0  ; -> 0026D6D0 fn
003B702C  inc      edi
003B702E  cmp      edi, r12d
003B7031  jl       0x3b6ff0  ; -> 003B6FF0
003B7033  inc      r15d
003B7036  cmp      r15d, 2
003B703A  jle      0x3b6fc6  ; -> 003B6FC6
003B703C  mov      ecx, dword ptr [rsp + 0x20]
003B7040  lea      r8, [rsp + 0x30]
003B7045  mov      edx, r14d
003B7048  call     0x3b6de0  ; -> 003B6DE0 fn
003B704D  mov      rcx, qword ptr [rsp + 0xb0]
003B7055  xor      rcx, rsp
003B7058  call     0x808c40  ; -> 00808C40 fn
003B705D  lea      r11, [rsp + 0xc0]
003B7065  mov      rbx, qword ptr [r11 + 0x38]
003B7069  mov      rbp, qword ptr [r11 + 0x40]
003B706D  mov      rsi, qword ptr [r11 + 0x48]
003B7071  mov      rsp, r11
003B7074  pop      r15
003B7076  pop      r14
003B7078  pop      r13
003B707A  pop      r12
003B707C  pop      rdi
003B707D  ret      
```

## 003D8300 (148 B, extent 003D8300-003D8394)

Page context: ", '3G@+0x80'-family); sub-update '0047BDA0' (128 B — **not** the 56 B base form; calls '002F2530' plus '003D8D70'/'003D8DE0' directly); sub-walk '0047BFA0' (8 B); sub-seventh '0047BF70' (36 B) calls '003D8300' on '+0x230'/'+0x234'. Its methods reach a '003D8xxx' helper family no other type in the band uses.  ## '0xA0'–'0xAB' — the top of the type space  Main-range '0xA0'/'0xA1'/'0xA2'/'0xA5'; sub-range '0xA3'/'0xA4'/'0xA6'–'0xAB' ('0xAC"

```
003D8300  push     rbx
003D8302  sub      rsp, 0x20
003D8306  lea      rax, [rip + 0x27754c3]  ; -> 02B4D7D0
003D830D  movzx    edx, cl
003D8310  lea      rbx, [rdx + rdx*2]
003D8314  shl      rbx, 5
003D8318  add      rbx, rax
003D831B  xor      eax, eax
003D831D  cmp      dword ptr [rbx + 4], ecx
003D8320  cmovne   rbx, rax
003D8324  test     rbx, rbx
003D8327  je       0x3d838e  ; -> 003D838E
003D8329  mov      ecx, dword ptr [rbx + 8]
003D832C  dec      byte ptr [rip + 0x277546e]  ; -> 02B4D7A0
003D8332  mov      dword ptr [rbx + 4], eax
003D8335  call     0x20e600  ; -> 0020E600 fn
003D833A  test     rax, rax
003D833D  je       0x3d834f  ; -> 003D834F
003D833F  mov      ecx, dword ptr [rbx + 8]
003D8342  call     0x20e600  ; -> 0020E600 fn
003D8347  mov      ecx, dword ptr [rbx + 0xc]
003D834A  mov      dword ptr [rax + 0xc], ecx
003D834D  jmp      0x3d835e  ; -> 003D835E
003D834F  mov      ecx, dword ptr [rbx + 0xc]
003D8352  call     0x20e600  ; -> 0020E600 fn
003D8357  mov      qword ptr [rip + 0x277544a], rax  ; -> 02B4D7A8
003D835E  mov      ecx, dword ptr [rbx + 0xc]
003D8361  call     0x20e600  ; -> 0020E600 fn
003D8366  test     rax, rax
003D8369  je       0x3d837f  ; -> 003D837F
003D836B  mov      ecx, dword ptr [rbx + 0xc]
003D836E  call     0x20e600  ; -> 0020E600 fn
003D8373  mov      ecx, dword ptr [rbx + 8]
003D8376  mov      dword ptr [rax + 8], ecx
003D8379  add      rsp, 0x20
003D837D  pop      rbx
003D837E  ret      
003D837F  mov      ecx, dword ptr [rbx + 8]
003D8382  call     0x20e600  ; -> 0020E600 fn
003D8387  mov      qword ptr [rip + 0x2775422], rax  ; -> 02B4D7B0
003D838E  add      rsp, 0x20
003D8392  pop      rbx
003D8393  ret      
```

## 003E4E70 (32 B, extent 003E4E70-003E4E90)

Page context: "ocabulary ('00464D41'–'00464E52'). '003B4A50' collects the records whose scope matches a character, and '003B4310' - called for 'CharacterRenderRecord_UpdateViewDependentPresentationFactors' through '003E4E70' - returns the one with the **lowest luminance '0.299 R + 0.587 G + 0.114 B' × strength** as that character's RGBA multiplier, '1,1,1,1' when none ('003B434A'–'003B435F', '003B4666'–'003B46C8'). Where several overlap, the darkest w"

```
003E4E70  sub      rsp, 0x28
003E4E74  movsx    ecx, word ptr [rcx]
003E4E77  call     0x3b4310  ; -> 003B4310 fn
003E4E7C  movss    xmm1, dword ptr [rip + 0x1906d24]  ; -> 01CEBBA8 [f32 1]
003E4E84  subss    xmm1, xmm0
003E4E88  movaps   xmm0, xmm1
003E4E8B  add      rsp, 0x28
003E4E8F  ret      
```

## 00460F30 (275 B, extent 00460F30-00461043)

Page context: "0xA3'/'0xA4'/'0xA6'–'0xAB' ('0xAC'+ are entirely absent — the tables admit them but every slot is default).  | type | methods | notes | |---|---|---| | '0xA0' | step '00460B80' (54 B: base+PRNG+tail '00460F30'), walk '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — t"

```
00460F30  mov      qword ptr [rsp + 8], rbx
00460F35  mov      qword ptr [rsp + 0x10], rbp
00460F3A  mov      qword ptr [rsp + 0x18], rsi
00460F3F  mov      qword ptr [rsp + 0x20], rdi
00460F44  push     r14
00460F46  sub      rsp, 0x20
00460F4A  mov      rsi, qword ptr [rcx + 0x20]
00460F4E  lea      rdi, [rcx + 0x230]
00460F55  mov      rbx, rcx
00460F58  lea      rcx, [rsi + 0xc0]
00460F5F  mov      edx, dword ptr [rbx + 0x44]
00460F62  call     0x42fdb0  ; -> 0042FDB0 fn
00460F67  mov      dword ptr [rdi], eax
00460F69  cmp      dword ptr [rbx + 0x1f0], 0x80808080
00460F73  je       0x460f87  ; -> 00460F87
00460F75  lea      r8, [rbx + 0x1f0]
00460F7C  mov      rdx, rdi
00460F7F  mov      rcx, rdi
00460F82  call     0x26ee00  ; -> 0026EE00 fn
00460F87  mov      edx, dword ptr [rbx + 0x44]
00460F8A  lea      rcx, [rsi + 0x110]
00460F91  call     0x42fdb0  ; -> 0042FDB0 fn
00460F96  mov      dword ptr [rbx + 0x234], eax
00460F9C  cmp      dword ptr [rbx + 0x1f0], 0x80808080
00460FA6  je       0x460fc2  ; -> 00460FC2
00460FA8  lea      r8, [rbx + 0x1f0]
00460FAF  lea      rdx, [rbx + 0x234]
00460FB6  lea      rcx, [rbx + 0x234]
00460FBD  call     0x26ee00  ; -> 0026EE00 fn
00460FC2  cmp      byte ptr [rsi + 0x49], 0x20
00460FC6  jb       0x461020  ; -> 00461020
00460FC8  mov      edx, dword ptr [rbx + 0x44]
00460FCB  lea      rcx, [rsi + 0x30]
00460FCF  call     0x4314e0  ; -> 004314E0 fn
00460FD4  mov      r8d, eax
00460FD7  cmp      eax, 0x64
00460FDA  je       0x461020  ; -> 00461020
00460FDC  movzx    ecx, byte ptr [rbx + 0x233]
00460FE3  mov      eax, 0x51eb851f
00460FE8  imul     ecx, r8d
00460FEC  imul     ecx
00460FEE  mov      eax, 0x51eb851f
00460FF3  sar      edx, 5
00460FF6  mov      ecx, edx
00460FF8  shr      ecx, 0x1f
00460FFB  add      edx, ecx
00460FFD  movzx    ecx, byte ptr [rbx + 0x237]
00461004  mov      byte ptr [rbx + 0x233], dl
0046100A  imul     ecx, r8d
0046100E  imul     ecx
00461010  sar      edx, 5
00461013  mov      eax, edx
00461015  shr      eax, 0x1f
00461018  add      edx, eax
0046101A  mov      byte ptr [rbx + 0x237], dl
00461020  mov      eax, dword ptr [rdi]
00461022  mov      rbp, qword ptr [rsp + 0x38]
00461027  mov      rsi, qword ptr [rsp + 0x40]
0046102C  mov      rdi, qword ptr [rsp + 0x48]
00461031  mov      dword ptr [rbx + 0x1f4], eax
00461037  mov      rbx, qword ptr [rsp + 0x30]
0046103C  add      rsp, 0x20
00461040  pop      r14
00461042  ret      
```

## 00461250 (25 B, extent 00461250-00461269)

Page context: "3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes | | '0xA2' | step '00462480' (177 B, '003D8E50'-family), walk '00462540' 2921 B | '0017FFD0'+'0024E2E0'/'0024E460'/'0024E640' VU0-path calls; set"

```
00461250  mov      rax, qword ptr [rcx + 0x20]
00461254  test     byte ptr [rax + 0x1b4], 4
0046125B  je       0x461268  ; -> 00461268
0046125D  mov      ecx, dword ptr [rcx + 0x294]
00461263  jmp      0x376990  ; -> 00376990 fn
00461268  ret      
```

## 00464050 (50 B, extent 00464050-00464082)

Page context: " of bit 1 in the element's byte '+0x248'*), setup   '0053AAC0' (80 B: base + '3G@+0x80' + '1T@+0xC0' + '4G@+0xD0'; the 'lea rax,   [rdi+0x130]' is the record-end return value, not a call),   seventh '00464050' (50 B) ~~calls '003ABCA0' on '+0x244'/'+0x24C'.~~ **Corrected 2026-09-29 (FABLE, GI-9):** two   different handles - it removes the light '+0x244' through '003ABCA0' and releases the registry slot '+0x24C' by   tail-jumping '003773"

```
00464050  push     rbx
00464052  sub      rsp, 0x20
00464056  mov      rbx, rcx
00464059  mov      ecx, dword ptr [rcx + 0x244]
0046405F  test     ecx, ecx
00464061  je       0x464072  ; -> 00464072
00464063  call     0x3abca0  ; -> 003ABCA0 fn
00464068  mov      dword ptr [rbx + 0x244], 0
00464072  mov      ecx, dword ptr [rbx + 0x24c]
00464078  add      rsp, 0x20
0046407C  pop      rbx
0046407D  jmp      0x377360  ; -> 00377360 fn
```

## 00464090 (8 B, extent 00464090-00464098)

Page context: "98217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the table/record interiors are not read everywhere; 00464090 read 2026-09-18 (an 8-byte setter of bit 1 in the element's +0x248, not a walk)" owner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721"

```
00464090  or       byte ptr [rcx + 0x248], 2
00464097  ret      
```

## 004649A0 (392 B, extent 004649A0-00464B28)

Page context: "he-element-types-60-74.md). **NATIVE/STATIC**; authority EXE '73461D08…21F8'.  ## '0x40' / '0x41' — minimal main-range types with a seventh  - '0x40': step '00463FF0' (81 B; base + '00377190' + tail '004649A0'), update the   56 B base+tail, walk '00464090' (8 B — *read 2026-09-18 (FABLE): not a walk at all; the whole body is 'or byte ptr [rcx+0x248], 2; ret', a setter of bit 1 in the element's byte '+0x248'*), setup   '0053AAC0' (80 B: "

```
004649A0  mov      qword ptr [rsp + 8], rbx
004649A5  mov      qword ptr [rsp + 0x10], rsi
004649AA  push     rdi
004649AB  sub      rsp, 0x30
004649AF  mov      rsi, qword ptr [rcx + 0x20]
004649B3  mov      rbx, rcx
004649B6  mov      r8d, dword ptr [rcx + 0x44]
004649BA  lea      rcx, [rsp + 0x20]
004649BF  lea      rdx, [rsi + 0x80]
004649C6  call     0x430b90  ; -> 00430B90 fn
004649CB  movaps   xmm0, xmmword ptr [rax]
004649CE  movdqa   xmmword ptr [rbx + 0x230], xmm0
004649D6  movups   xmm1, xmm0
004649D9  movups   xmmword ptr [rip + 0x1e74900], xmm0  ; -> 022D92E0
004649E0  movups   xmm2, xmmword ptr [rbx + 0x60]
004649E4  movss    xmm0, dword ptr [rip + 0x1e748f8]  ; -> 022D92E4
004649EC  addss    xmm1, xmm2
004649F0  movups   xmmword ptr [rip + 0x1e748f9], xmm2  ; -> 022D92F0
004649F7  movss    dword ptr [rip + 0x1e748e1], xmm1  ; -> 022D92E0
004649FF  movaps   xmm1, xmm2
00464A02  shufps   xmm1, xmm2, 0x55
00464A06  addss    xmm0, xmm1
00464A0A  movaps   xmm1, xmm2
00464A0D  shufps   xmm1, xmm2, 0xaa
00464A11  shufps   xmm2, xmm2, 0xff
00464A15  movss    dword ptr [rip + 0x1e748c7], xmm0  ; -> 022D92E4
00464A1D  movss    xmm0, dword ptr [rip + 0x1e748c3]  ; -> 022D92E8
00464A25  addss    xmm0, xmm1
00464A29  movss    dword ptr [rip + 0x1e748b7], xmm0  ; -> 022D92E8
00464A31  movss    xmm0, dword ptr [rip + 0x1e748b3]  ; -> 022D92EC
00464A39  addss    xmm0, xmm2
00464A3D  movss    dword ptr [rip + 0x1e748a7], xmm0  ; -> 022D92EC
00464A45  movups   xmm0, xmmword ptr [rip + 0x1e74894]  ; -> 022D92E0
00464A4C  movups   xmmword ptr [rbx + 0x230], xmm0
00464A53  mov      rcx, qword ptr [rbx + 0x10]
00464A57  test     rcx, rcx
00464A5A  je       0x464a78  ; -> 00464A78
00464A5C  add      rcx, 0x40
00464A60  call     0x39af70  ; -> 0039AF70 fn
00464A65  lea      rdx, [rbx + 0x230]
00464A6C  lea      rcx, [rbx + 0x230]
00464A73  call     0x398f90  ; -> 00398F90 fn
00464A78  movaps   xmm0, xmmword ptr [rbx + 0x70]
00464A7C  lea      rcx, [rsi + 0xd0]
00464A83  mov      edx, dword ptr [rbx + 0x44]
00464A86  movdqa   xmmword ptr [rbx + 0x80], xmm0
00464A8E  movaps   xmm1, xmmword ptr [rbx + 0x230]
00464A95  movdqa   xmmword ptr [rbx + 0x70], xmm1
00464A9A  call     0x42fdb0  ; -> 0042FDB0 fn
00464A9F  lea      r8, [rbx + 0x1f0]
00464AA6  mov      dword ptr [rbx + 0x240], eax
00464AAC  cmp      dword ptr [r8], 0x80808080
00464AB3  je       0x464ac8  ; -> 00464AC8
00464AB5  lea      rdx, [rbx + 0x240]
00464ABC  lea      rcx, [rbx + 0x240]
00464AC3  call     0x26ee00  ; -> 0026EE00 fn
00464AC8  cmp      byte ptr [rsi + 0x49], 0x20
00464ACC  jb       0x464b00  ; -> 00464B00
00464ACE  mov      edx, dword ptr [rbx + 0x44]
00464AD1  lea      rcx, [rsi + 0x30]
00464AD5  call     0x4314e0  ; -> 004314E0 fn
00464ADA  cmp      eax, 0x64
00464ADD  je       0x464b00  ; -> 00464B00
00464ADF  movzx    ecx, byte ptr [rbx + 0x243]
00464AE6  imul     ecx, eax
00464AE9  mov      eax, 0x51eb851f
00464AEE  imul     ecx
00464AF0  sar      edx, 5
00464AF3  mov      eax, edx
00464AF5  shr      eax, 0x1f
00464AF8  add      edx, eax
00464AFA  mov      byte ptr [rbx + 0x243], dl
00464B00  mov      eax, dword ptr [rbx + 0x240]
00464B06  mov      rdx, rbx
00464B09  mov      ecx, 2
00464B0E  mov      dword ptr [rbx + 0x1f4], eax
00464B14  mov      rbx, qword ptr [rsp + 0x40]
00464B19  mov      rsi, qword ptr [rsp + 0x48]
00464B1E  add      rsp, 0x30
00464B22  pop      rdi
00464B23  jmp      0x3a8950  ; -> 003A8950 fn
```

## 00464B80 (50 B, extent 00464B80-00464BB2)

Page context: "**5 B stub** (shared with '0xD0'),   walk '00464BC0' 8 B, setup '0053AB10' 52 B (base + '4G@+0x80' only; 'lea rax,   [rdi+0xE0]' is the record-end return value — there is no '+0xE0' call),   seventh '00464B80' (50 B) calls '003B42B0' on '+0x234'/'+0x238'. These are the   thinnest handled types: nearly everything falls through to base/no-op.  ## '0x42' — the lone bottom of the sub-range  Sub-range only (main dispatchers all 'default'). S"

```
00464B80  push     rbx
00464B82  sub      rsp, 0x20
00464B86  mov      rbx, rcx
00464B89  mov      ecx, dword ptr [rcx + 0x234]
00464B8F  test     ecx, ecx
00464B91  je       0x464ba2  ; -> 00464BA2
00464B93  call     0x3b42b0  ; -> 003B42B0 fn
00464B98  mov      dword ptr [rbx + 0x234], 0
00464BA2  mov      ecx, dword ptr [rbx + 0x238]
00464BA8  add      rsp, 0x20
00464BAC  pop      rbx
00464BAD  jmp      0x377360  ; -> 00377360 fn
```

## 00464BC0 (8 B, extent 00464BC0-00464BC8)

Page context: "C' by   tail-jumping '00377360' ([what these types are](#what-these-seven-types-are-gi-9-2026-09-29-fable)). - '0x41': even smaller — update '00464F10' is a **5 B stub** (shared with '0xD0'),   walk '00464BC0' 8 B, setup '0053AB10' 52 B (base + '4G@+0x80' only; 'lea rax,   [rdi+0xE0]' is the record-end return value — there is no '+0xE0' call),   seventh '00464B80' (50 B) calls '003B42B0' on '+0x234'/'+0x238'. These are the   thinnest ha"

```
00464BC0  or       byte ptr [rcx + 0x23c], 1
00464BC7  ret      
```

## 0047BF70 (36 B, extent 0047BF70-0047BF94)

Page context: "b-setup '0050C450' (80 B, '3G@+0x80'-family); sub-update '0047BDA0' (128 B — **not** the 56 B base form; calls '002F2530' plus '003D8D70'/'003D8DE0' directly); sub-walk '0047BFA0' (8 B); sub-seventh '0047BF70' (36 B) calls '003D8300' on '+0x230'/'+0x234'. Its methods reach a '003D8xxx' helper family no other type in the band uses.  ## '0xA0'–'0xAB' — the top of the type space  Main-range '0xA0'/'0xA1'/'0xA2'/'0xA5'; sub-range '0xA3'/'0x"

```
0047BF70  push     rbx
0047BF72  sub      rsp, 0x20
0047BF76  mov      rbx, rcx
0047BF79  mov      ecx, dword ptr [rcx + 0x230]
0047BF7F  call     0x3d8300  ; -> 003D8300 fn
0047BF84  mov      ecx, dword ptr [rbx + 0x234]
0047BF8A  add      rsp, 0x20
0047BF8E  pop      rbx
0047BF8F  jmp      0x377360  ; -> 00377360 fn
```

## 004CF490 (5098 B, extent 004CF490-004D087A)

Page context: "E9D50' with its A+D data preset to '0x42' / '0x1001' / '0x45' at '+0x130' / '+0x140' / '+0x150' ('0054B6B8'–'0054B836') | | '+0x30', '+0x40' | the head of template '02AEC4B0' - the one that installs '004CF490' - and its body at '+0x360' ('0x190' bytes) carrying the caller's matrix '[rdx+0x18]', vector '[rdx]' and float '[rdx+0x10]' ('0054B84C'–'0054B90E') | | '+0x50', '+0x60' | '02AE9BC0' and '02AE9BE0' **again** ('0054B66D'–'0054B695')"

```
004CF490  mov      rax, rsp
004CF493  mov      qword ptr [rax + 0x18], rbx
004CF497  push     rbp
004CF498  push     rsi
004CF499  push     rdi
004CF49A  push     r12
004CF49C  push     r13
004CF49E  push     r14
004CF4A0  push     r15
004CF4A2  sub      rsp, 0xd0
004CF4A9  movsx    r10d, word ptr [rip + 0x1b9565b]  ; -> 02064B0C
004CF4B1  lea      rbx, [rip + 0x1b95978]  ; -> 02064E30
004CF4B8  movaps   xmmword ptr [rax - 0x48], xmm6
004CF4BC  mov      r13, rcx
004CF4BF  movaps   xmmword ptr [rax - 0x58], xmm7
004CF4C3  movaps   xmmword ptr [rax - 0x68], xmm8
004CF4C8  movaps   xmmword ptr [rax - 0x78], xmm9
004CF4CD  movaps   xmmword ptr [rax - 0x88], xmm10
004CF4D5  lea      eax, [r10 + 1]
004CF4D9  shl      eax, 4
004CF4DC  movsxd   r8, eax
004CF4DF  lea      eax, [r10 + 2]
004CF4E3  shl      eax, 4
004CF4E6  movsxd   rcx, eax
004CF4E9  lea      eax, [r10 + 3]
004CF4ED  shl      eax, 4
004CF4F0  movups   xmm0, xmmword ptr [r8 + rbx]
004CF4F5  mov      word ptr [rip + 0x1b958bb], r10w  ; -> 02064DB8
004CF4FD  movups   xmm3, xmmword ptr [rcx + rbx]
004CF501  movsxd   rcx, eax
004CF504  movaps   xmmword ptr [rsp + 0x70], xmm11
004CF50A  movaps   xmmword ptr [rsp + 0x60], xmm12
004CF510  movaps   xmmword ptr [rsp + 0x50], xmm13
004CF516  movaps   xmmword ptr [rsp + 0x40], xmm14
004CF51C  movaps   xmmword ptr [rsp + 0x30], xmm15
004CF522  lea      eax, [r10 + 4]
004CF526  mov      word ptr [rip + 0x1b958a2], r10w  ; -> 02064DD0
004CF52E  movups   xmm4, xmmword ptr [rcx + rbx]
004CF532  shl      eax, 4
004CF535  movsxd   rcx, eax
004CF538  lea      eax, [r10 + 5]
004CF53C  shl      eax, 4
004CF53F  movaps   xmm1, xmm4
004CF542  movups   xmmword ptr [rip + 0x1b955e7], xmm0  ; -> 02064B30
004CF549  mov      qword ptr [rsp + 0x20], rdx
004CF54E  movups   xmm0, xmmword ptr [rcx + rbx]
004CF552  movsxd   rcx, eax
004CF555  lea      eax, [r10 + 6]
004CF559  shl      eax, 4
004CF55C  movaps   xmm2, xmm4
004CF55F  movups   xmmword ptr [rip + 0x1b955fa], xmm0  ; -> 02064B60
004CF566  mov      dword ptr [rip + 0x1b95594], 0x3f000000  ; -> 02064B04
004CF570  movups   xmm0, xmmword ptr [rcx + rbx]
004CF574  movsxd   rcx, eax
004CF577  lea      eax, [r10 + 7]
004CF57B  shl      eax, 4
004CF57E  movups   xmmword ptr [rip + 0x1b955eb], xmm0  ; -> 02064B70
004CF585  movups   xmm0, xmmword ptr [rcx + rbx]
004CF589  movsxd   rcx, eax
004CF58C  lea      eax, [r10 + 8]
004CF590  shl      eax, 4
004CF593  movups   xmmword ptr [rip + 0x1b955e6], xmm0  ; -> 02064B80
004CF59A  movups   xmm0, xmmword ptr [rcx + rbx]
004CF59E  movsxd   rcx, eax
004CF5A1  lea      eax, [r10 + 9]
004CF5A5  shl      eax, 4
004CF5A8  movups   xmmword ptr [rip + 0x1b95591], xmm3  ; -> 02064B40
004CF5AF  mulss    xmm3, dword ptr [rip + 0x181c5b9]  ; -> 01CEBB70 [f32 0.5]
004CF5B7  shufps   xmm1, xmm4, 0x55
004CF5BB  movups   xmmword ptr [rip + 0x1b955ce], xmm0  ; -> 02064B90
004CF5C2  movups   xmm0, xmmword ptr [rcx + rbx]
004CF5C6  movsxd   rcx, eax
004CF5C9  mov      eax, 0x12c
004CF5CE  add      eax, r10d
004CF5D1  mulss    xmm2, xmm3
004CF5D5  mov      word ptr [rip + 0x1b957d4], ax  ; -> 02064DB0
004CF5DC  inc      ax
004CF5DF  movups   xmmword ptr [rip + 0x1b9556a], xmm4  ; -> 02064B50
004CF5E6  mov      word ptr [rip + 0x1b957c7], ax  ; -> 02064DB4
004CF5ED  lea      eax, [r10 + 0x64]
004CF5F1  movups   xmmword ptr [rip + 0x1b955a8], xmm0  ; -> 02064BA0
004CF5F8  add      r10w, 0xa
004CF5FD  mov      word ptr [rip + 0x1b957b8], ax  ; -> 02064DBC
004CF604  movups   xmm0, xmmword ptr [rcx + rbx]
004CF608  mov      word ptr [rip + 0x1b957b0], r10w  ; -> 02064DC0
004CF610  mulss    xmm1, xmm3
004CF614  shufps   xmm4, xmm4, 0xaa
004CF618  movss    dword ptr [rip + 0x1b95520], xmm2  ; -> 02064B40
004CF620  movss    dword ptr [rip + 0x1b9551c], xmm1  ; -> 02064B44
004CF628  movups   xmmword ptr [rip + 0x1b95581], xmm0  ; -> 02064BB0
004CF62F  mulss    xmm4, xmm3
004CF633  movss    xmm0, dword ptr [rip + 0x19331f9]  ; -> 01E02834 [u32 0x00000000]
004CF63B  addss    xmm0, xmm1
004CF63F  movss    dword ptr [rip + 0x1b95501], xmm4  ; -> 02064B48
004CF647  movss    xmm1, dword ptr [rip + 0x19331e1]  ; -> 01E02830 [u32 0x00000000]
004CF64F  subss    xmm1, xmm2
004CF653  movss    dword ptr [rip + 0x1b95649], xmm0  ; -> 02064CA4
004CF65B  movss    xmm0, dword ptr [rip + 0x19331d9]  ; -> 01E0283C [f32 1]
004CF663  movss    dword ptr [rip + 0x1b956b1], xmm0  ; -> 02064D1C
004CF66B  movss    xmm0, dword ptr [rip + 0x19331c5]  ; -> 01E02838 [u32 0x00000000]
004CF673  subss    xmm0, xmm4
004CF677  movss    dword ptr [rip + 0x1b95621], xmm1  ; -> 02064CA0
004CF67F  movss    dword ptr [rip + 0x1b95621], xmm0  ; -> 02064CA8
004CF687  call     0x22cc20  ; -> 0022CC20 fn
004CF68C  movss    xmm1, dword ptr [rip + 0x19331a4]  ; -> 01E02838 [u32 0x00000000]
004CF694  addss    xmm1, dword ptr [rip + 0x1b954ac]  ; -> 02064B48
004CF69C  movss    xmm0, dword ptr [rip + 0x1933190]  ; -> 01E02834 [u32 0x00000000]
004CF6A4  addss    xmm0, dword ptr [rip + 0x1b95498]  ; -> 02064B44
004CF6AC  movss    dword ptr [rip + 0x1b95604], xmm1  ; -> 02064CB8
004CF6B4  movss    xmm1, dword ptr [rip + 0x1933174]  ; -> 01E02830 [u32 0x00000000]
004CF6BC  subss    xmm1, dword ptr [rip + 0x1b9547c]  ; -> 02064B40
004CF6C4  movss    dword ptr [rip + 0x1b955e8], xmm0  ; -> 02064CB4
004CF6CC  movss    xmm0, dword ptr [rip + 0x1933168]  ; -> 01E0283C [f32 1]
004CF6D4  movss    dword ptr [rip + 0x1b95630], xmm0  ; -> 02064D0C
004CF6DC  movss    dword ptr [rip + 0x1b955cc], xmm1  ; -> 02064CB0
004CF6E4  call     0x22cc20  ; -> 0022CC20 fn
004CF6E9  movss    xmm4, dword ptr [rip + 0x1933147]  ; -> 01E02838 [u32 0x00000000]
004CF6F1  movss    xmm1, dword ptr [rip + 0x1933143]  ; -> 01E0283C [f32 1]
004CF6F9  movaps   xmm0, xmm4
004CF6FC  movss    xmm5, dword ptr [rip + 0x193312c]  ; -> 01E02830 [u32 0x00000000]
004CF704  addss    xmm5, dword ptr [rip + 0x1b95434]  ; -> 02064B40
004CF70C  movss    xmm3, dword ptr [rip + 0x1933120]  ; -> 01E02834 [u32 0x00000000]
004CF714  addss    xmm3, dword ptr [rip + 0x1b95428]  ; -> 02064B44
004CF71C  addss    xmm0, dword ptr [rip + 0x1b95424]  ; -> 02064B48
004CF724  subss    xmm4, dword ptr [rip + 0x1b9541c]  ; -> 02064B48
004CF72C  movss    dword ptr [rip + 0x1b9558c], xmm5  ; -> 02064CC0
004CF734  movss    dword ptr [rip + 0x1b955c0], xmm1  ; -> 02064CFC
004CF73C  movss    dword ptr [rip + 0x1b95580], xmm3  ; -> 02064CC4
004CF744  movss    dword ptr [rip + 0x1b9557c], xmm0  ; -> 02064CC8
004CF74C  movss    dword ptr [rip + 0x1b9557c], xmm5  ; -> 02064CD0
004CF754  movss    dword ptr [rip + 0x1b95578], xmm3  ; -> 02064CD4
004CF75C  movss    dword ptr [rip + 0x1b95588], xmm1  ; -> 02064CEC
004CF764  movss    dword ptr [rip + 0x1b9556c], xmm4  ; -> 02064CD8
004CF76C  call     0x22cc20  ; -> 0022CC20 fn
004CF771  movss    xmm0, dword ptr [rip + 0x19330b7]  ; -> 01E02830 [u32 0x00000000]
004CF779  subss    xmm0, dword ptr [rip + 0x1b953bf]  ; -> 02064B40
004CF781  movss    xmm1, dword ptr [rip + 0x19330ab]  ; -> 01E02834 [u32 0x00000000]
004CF789  subss    xmm1, dword ptr [rip + 0x1b953b3]  ; -> 02064B44
004CF791  movss    dword ptr [rip + 0x1b95547], xmm0  ; -> 02064CE0
004CF799  movss    xmm0, dword ptr [rip + 0x1933097]  ; -> 01E02838 [u32 0x00000000]
004CF7A1  subss    xmm0, dword ptr [rip + 0x1b9539f]  ; -> 02064B48
004CF7A9  movss    dword ptr [rip + 0x1b95533], xmm1  ; -> 02064CE4
004CF7B1  movss    dword ptr [rip + 0x1b9552f], xmm0  ; -> 02064CE8
004CF7B9  call     0x22cc20  ; -> 0022CC20 fn
004CF7BE  movss    xmm0, dword ptr [rip + 0x1933072]  ; -> 01E02838 [u32 0x00000000]
004CF7C6  xorps    xmm8, xmm8
004CF7CA  addss    xmm0, dword ptr [rip + 0x1b95376]  ; -> 02064B48
004CF7D2  movss    xmm1, dword ptr [rip + 0x1933062]  ; -> 01E0283C [f32 1]
004CF7DA  movss    xmm2, dword ptr [rip + 0x193304e]  ; -> 01E02830 [u32 0x00000000]
004CF7E2  subss    xmm2, dword ptr [rip + 0x1b95356]  ; -> 02064B40
004CF7EA  movss    dword ptr [rip + 0x1b954ea], xmm1  ; -> 02064CDC
004CF7F2  movss    dword ptr [rip + 0x1b954fe], xmm0  ; -> 02064CF8
004CF7FA  movss    xmm0, dword ptr [rip + 0x1933032]  ; -> 01E02834 [u32 0x00000000]
004CF802  subss    xmm0, dword ptr [rip + 0x1b9533a]  ; -> 02064B44
004CF80A  ucomiss  xmm2, xmm8
004CF80E  movss    dword ptr [rip + 0x1b954de], xmm0  ; -> 02064CF4
004CF816  movss    dword ptr [rip + 0x1b9548e], xmm1  ; -> 02064CAC
004CF81E  movss    dword ptr [rip + 0x1b954ca], xmm2  ; -> 02064CF0
004CF826  jp       0x4cf82a  ; -> 004CF82A
004CF828  je       0x4cf832  ; -> 004CF832
004CF82A  ucomiss  xmm0, xmm8
004CF82E  jp       0x4cf847  ; -> 004CF847
004CF830  jne      0x4cf847  ; -> 004CF847
004CF832  call     0x22cc40  ; -> 0022CC40 fn
004CF837  movss    xmm0, dword ptr [rip + 0x1b954b5]  ; -> 02064CF4
004CF83F  movss    xmm2, dword ptr [rip + 0x1b954a9]  ; -> 02064CF0
004CF847  comiss   xmm8, xmm2
004CF84B  ja       0x4cf853  ; -> 004CF853
004CF84D  comiss   xmm8, xmm0
004CF851  jbe      0x4cf858  ; -> 004CF858
004CF853  call     0x22cc30  ; -> 0022CC30 fn
004CF858  call     0x22cc20  ; -> 0022CC20 fn
004CF85D  movss    xmm1, dword ptr [rip + 0x1932fd3]  ; -> 01E02838 [u32 0x00000000]
004CF865  addss    xmm1, dword ptr [rip + 0x1b952db]  ; -> 02064B48
004CF86D  movss    xmm0, dword ptr [rip + 0x1932fbb]  ; -> 01E02830 [u32 0x00000000]
004CF875  addss    xmm0, dword ptr [rip + 0x1b952c3]  ; -> 02064B40
004CF87D  movss    dword ptr [rip + 0x1b95483], xmm1  ; -> 02064D08
004CF885  movss    xmm1, dword ptr [rip + 0x1932fa7]  ; -> 01E02834 [u32 0x00000000]
004CF88D  subss    xmm1, dword ptr [rip + 0x1b952af]  ; -> 02064B44
004CF895  movss    dword ptr [rip + 0x1b95463], xmm0  ; -> 02064D00
004CF89D  movss    xmm0, dword ptr [rip + 0x1932f97]  ; -> 01E0283C [f32 1]
004CF8A5  movss    dword ptr [rip + 0x1b9540f], xmm0  ; -> 02064CBC
004CF8AD  movss    dword ptr [rip + 0x1b9544f], xmm1  ; -> 02064D04
004CF8B5  call     0x22cc20  ; -> 0022CC20 fn
004CF8BA  movss    xmm0, dword ptr [rip + 0x1932f6e]  ; -> 01E02830 [u32 0x00000000]
004CF8C2  addss    xmm0, dword ptr [rip + 0x1b95276]  ; -> 02064B40
004CF8CA  movss    xmm1, dword ptr [rip + 0x1932f62]  ; -> 01E02834 [u32 0x00000000]
004CF8D2  subss    xmm1, dword ptr [rip + 0x1b9526a]  ; -> 02064B44
004CF8DA  movss    dword ptr [rip + 0x1b9542e], xmm0  ; -> 02064D10
004CF8E2  movss    xmm0, dword ptr [rip + 0x1932f52]  ; -> 01E0283C [f32 1]
004CF8EA  movss    dword ptr [rip + 0x1b953da], xmm0  ; -> 02064CCC
004CF8F2  movss    xmm0, dword ptr [rip + 0x1932f3e]  ; -> 01E02838 [u32 0x00000000]
004CF8FA  subss    xmm0, dword ptr [rip + 0x1b95246]  ; -> 02064B48
004CF902  movss    dword ptr [rip + 0x1b9540a], xmm1  ; -> 02064D14
004CF90A  movss    dword ptr [rip + 0x1b95406], xmm0  ; -> 02064D18
004CF912  call     0x22cc20  ; -> 0022CC20 fn
004CF917  movsx    edi, word ptr [rip + 0x1b9549e]  ; -> 02064DBC
004CF91E  mov      r12d, 0xe0
004CF924  movups   xmm0, xmmword ptr [rip + 0x1b95375]  ; -> 02064CA0
004CF92B  movzx    r15d, word ptr [rip + 0x1b951d9]  ; -> 02064B0C
004CF933  mov      ecx, edi
004CF935  movss    xmm10, dword ptr [rip + 0x1b951fa]  ; -> 02064B38
004CF93E  movss    xmm9, dword ptr [rip + 0x1b951ed]  ; -> 02064B34
004CF947  movss    xmm11, dword ptr [rip + 0x1b951e0]  ; -> 02064B30
004CF950  movss    xmm13, dword ptr [rip + 0x1932edf]  ; -> 01E02838 [u32 0x00000000]
004CF959  lea      r14d, [r15 + 4]
004CF95D  movss    xmm12, dword ptr [rip + 0x1932ece]  ; -> 01E02834 [u32 0x00000000]
004CF966  movss    xmm14, dword ptr [rip + 0x1932ec1]  ; -> 01E02830 [u32 0x00000000]
004CF96F  movss    xmm15, dword ptr [rip + 0x4309e8]  ; -> 00900360 [u32 0x7F7FFFFF]
004CF978  shl      ecx, 4
004CF97B  movsxd   rax, ecx
004CF97E  movups   xmmword ptr [rax + rbx], xmm0
004CF982  lea      eax, [rcx + 0x10]
004CF985  movups   xmm0, xmmword ptr [rip + 0x1b95324]  ; -> 02064CB0
004CF98C  movsxd   rcx, eax
004CF98F  lea      eax, [rdi + 2]
004CF992  shl      eax, 4
004CF995  movups   xmmword ptr [rcx + rbx], xmm0
004CF999  movsxd   rcx, eax
004CF99C  lea      eax, [rdi + 3]
004CF99F  movups   xmm0, xmmword ptr [rip + 0x1b9531a]  ; -> 02064CC0
004CF9A6  shl      eax, 4
004CF9A9  movups   xmmword ptr [rcx + rbx], xmm0
004CF9AD  movsxd   rcx, eax
004CF9B0  lea      eax, [rdi + 4]
004CF9B3  movups   xmm0, xmmword ptr [rip + 0x1b95316]  ; -> 02064CD0
004CF9BA  shl      eax, 4
004CF9BD  movups   xmmword ptr [rcx + rbx], xmm0
004CF9C1  movsxd   rcx, eax
004CF9C4  lea      eax, [rdi + 5]
004CF9C7  movups   xmm0, xmmword ptr [rip + 0x1b95312]  ; -> 02064CE0
004CF9CE  shl      eax, 4
004CF9D1  movups   xmmword ptr [rcx + rbx], xmm0
004CF9D5  movsxd   rcx, eax
004CF9D8  lea      eax, [rdi + 6]
004CF9DB  movups   xmm0, xmmword ptr [rip + 0x1b9530e]  ; -> 02064CF0
004CF9E2  shl      eax, 4
004CF9E5  movups   xmmword ptr [rcx + rbx], xmm0
004CF9E9  movsxd   rcx, eax
004CF9EC  lea      eax, [rdi + 7]
004CF9EF  movups   xmm0, xmmword ptr [rip + 0x1b9530a]  ; -> 02064D00
004CF9F6  shl      eax, 4
004CF9F9  add      di, r15w
004CF9FD  add      r12d, r15d
004CFA00  movups   xmmword ptr [rcx + rbx], xmm0
004CFA04  movsxd   rcx, eax
004CFA07  movups   xmm0, xmmword ptr [rip + 0x1b95302]  ; -> 02064D10
004CFA0E  movups   xmmword ptr [rcx + rbx], xmm0
004CFA12  nop      dword ptr [rax]
004CFA16  nop      word ptr [rax + rax]
004CFA20  movss    xmm1, dword ptr [rip + 0x1b95150]  ; -> 02064B78
004CFA28  dec      r14w
004CFA2C  movsx    eax, di
004CFA2F  shl      eax, 4
004CFA32  movsxd   rsi, eax
004CFA35  add      eax, 0x10
004CFA38  movsxd   rbp, eax
004CFA3B  movups   xmm7, xmmword ptr [rsi + rbx]
004CFA3F  movups   xmm0, xmmword ptr [rbx + rbp]
004CFA43  movups   xmmword ptr [rip + 0x1b95266], xmm7  ; -> 02064CB0
004CFA4A  movups   xmmword ptr [rip + 0x1b9526f], xmm0  ; -> 02064CC0
004CFA51  movups   xmm0, xmmword ptr [rip + 0x1b95108]  ; -> 02064B60
004CFA58  movaps   xmm6, xmm7
004CFA5B  movaps   xmm2, xmm7
004CFA5E  shufps   xmm2, xmm7, 0x55
004CFA62  mulss    xmm1, xmm2
004CFA66  shufps   xmm6, xmm6, 0
004CFA6A  mulps    xmm6, xmm0
004CFA6D  movss    xmm0, dword ptr [rip + 0x1b950fb]  ; -> 02064B70
004CFA75  mulss    xmm0, xmm2
004CFA79  movups   xmmword ptr [rip + 0x1b950a0], xmm6  ; -> 02064B20
004CFA80  movss    xmm3, dword ptr [rip + 0x1b9509c]  ; -> 02064B24
004CFA88  addss    xmm6, xmm0
004CFA8C  movss    xmm0, dword ptr [rip + 0x1b950e0]  ; -> 02064B74
004CFA94  movss    xmm4, dword ptr [rip + 0x1b9508c]  ; -> 02064B28
004CFA9C  movss    xmm5, dword ptr [rip + 0x1b95088]  ; -> 02064B2C
004CFAA4  addss    xmm4, xmm1
004CFAA8  movss    xmm1, dword ptr [rip + 0x1b950d0]  ; -> 02064B80
004CFAB0  mulss    xmm0, xmm2
004CFAB4  addss    xmm3, xmm0
004CFAB8  movss    xmm0, dword ptr [rip + 0x1b950bc]  ; -> 02064B7C
004CFAC0  mulss    xmm0, xmm2
004CFAC4  movaps   xmm2, xmm7
004CFAC7  shufps   xmm2, xmm7, 0xaa
004CFACB  mulss    xmm1, xmm2
004CFACF  addss    xmm5, xmm0
004CFAD3  shufps   xmm7, xmm7, 0xff
004CFAD7  movss    xmm0, dword ptr [rip + 0x1b950a5]  ; -> 02064B84
004CFADF  mulss    xmm0, xmm2
004CFAE3  addss    xmm6, xmm1
004CFAE7  movss    xmm1, dword ptr [rip + 0x1b95099]  ; -> 02064B88
004CFAEF  mulss    xmm1, xmm2
004CFAF3  addss    xmm3, xmm0
004CFAF7  movss    xmm0, dword ptr [rip + 0x1b9508d]  ; -> 02064B8C
004CFAFF  mulss    xmm0, xmm2
004CFB03  movss    xmm2, dword ptr [rip + 0x1b95091]  ; -> 02064B9C
004CFB0B  addss    xmm4, xmm1
004CFB0F  movss    xmm1, dword ptr [rip + 0x1b95079]  ; -> 02064B90
004CFB17  mulss    xmm1, xmm7
004CFB1B  addss    xmm5, xmm0
004CFB1F  movss    xmm0, dword ptr [rip + 0x1b9506d]  ; -> 02064B94
004CFB27  mulss    xmm2, xmm7
004CFB2B  addss    xmm1, xmm6
004CFB2F  mulss    xmm0, xmm7
004CFB33  addss    xmm2, xmm5
004CFB37  addss    xmm0, xmm3
004CFB3B  movss    dword ptr [rip + 0x1b9516d], xmm1  ; -> 02064CB0
004CFB43  movss    xmm1, dword ptr [rip + 0x1b9504d]  ; -> 02064B98
004CFB4B  ucomiss  xmm2, xmm8
004CFB4F  mulss    xmm1, xmm7
004CFB53  movss    dword ptr [rip + 0x1b95159], xmm0  ; -> 02064CB4
004CFB5B  movss    dword ptr [rip + 0x1b95159], xmm2  ; -> 02064CBC
004CFB63  addss    xmm1, xmm4
004CFB67  movss    dword ptr [rip + 0x1b95149], xmm1  ; -> 02064CB8
004CFB6F  jp       0x4cfb81  ; -> 004CFB81
004CFB71  jne      0x4cfb81  ; -> 004CFB81
004CFB73  movss    xmm7, dword ptr [rip + 0x1932cc1]  ; -> 01E0283C [f32 1]
004CFB7B  movaps   xmm0, xmm15
004CFB7F  jmp      0x4cfb90  ; -> 004CFB90
004CFB81  movss    xmm7, dword ptr [rip + 0x1932cb3]  ; -> 01E0283C [f32 1]
004CFB89  movaps   xmm0, xmm7
004CFB8C  divss    xmm0, xmm2
004CFB90  movss    xmm2, dword ptr [rip + 0x1b9512c]  ; -> 02064CC4
004CFB98  movups   xmm1, xmmword ptr [rip + 0x1b95111]  ; -> 02064CB0
004CFB9F  movss    xmm6, dword ptr [rip + 0x1b95119]  ; -> 02064CC0
004CFBA7  shufps   xmm0, xmm0, 0
004CFBAB  mulps    xmm1, xmm0
004CFBAE  movups   xmm0, xmmword ptr [rip + 0x1b94fab]  ; -> 02064B60
004CFBB5  shufps   xmm6, xmm6, 0
004CFBB9  mulps    xmm6, xmm0
004CFBBC  movss    xmm0, dword ptr [rip + 0x1b94fac]  ; -> 02064B70
004CFBC4  mulss    xmm0, xmm2
004CFBC8  movups   xmmword ptr [rip + 0x1b950e1], xmm1  ; -> 02064CB0
004CFBCF  movss    xmm1, dword ptr [rip + 0x1b94fa1]  ; -> 02064B78
004CFBD7  mulss    xmm1, xmm2
004CFBDB  movups   xmmword ptr [rip + 0x1b94f3e], xmm6  ; -> 02064B20
004CFBE2  movss    xmm3, dword ptr [rip + 0x1b94f3a]  ; -> 02064B24
004CFBEA  addss    xmm6, xmm0
004CFBEE  movss    xmm0, dword ptr [rip + 0x1b94f7e]  ; -> 02064B74
004CFBF6  movss    xmm4, dword ptr [rip + 0x1b94f2a]  ; -> 02064B28
004CFBFE  movss    xmm5, dword ptr [rip + 0x1b94f26]  ; -> 02064B2C
004CFC06  addss    xmm4, xmm1
004CFC0A  movss    xmm1, dword ptr [rip + 0x1b94f6e]  ; -> 02064B80
004CFC12  mulss    xmm0, xmm2
004CFC16  addss    xmm3, xmm0
004CFC1A  movss    xmm0, dword ptr [rip + 0x1b94f5a]  ; -> 02064B7C
004CFC22  mulss    xmm0, xmm2
004CFC26  movss    xmm2, dword ptr [rip + 0x1b9509a]  ; -> 02064CC8
004CFC2E  mulss    xmm1, xmm2
004CFC32  addss    xmm5, xmm0
004CFC36  movss    xmm0, dword ptr [rip + 0x1b94f46]  ; -> 02064B84
004CFC3E  mulss    xmm0, xmm2
004CFC42  addss    xmm6, xmm1
004CFC46  movss    xmm1, dword ptr [rip + 0x1b94f3a]  ; -> 02064B88
004CFC4E  mulss    xmm1, xmm2
004CFC52  addss    xmm3, xmm0
004CFC56  movss    xmm0, dword ptr [rip + 0x1b94f2e]  ; -> 02064B8C
004CFC5E  mulss    xmm0, xmm2
004CFC62  movss    xmm2, dword ptr [rip + 0x1b95062]  ; -> 02064CCC
004CFC6A  addss    xmm4, xmm1
004CFC6E  movss    xmm1, dword ptr [rip + 0x1b94f1a]  ; -> 02064B90
004CFC76  addss    xmm5, xmm0
004CFC7A  mulss    xmm1, xmm2
004CFC7E  movss    xmm0, dword ptr [rip + 0x1b94f0e]  ; -> 02064B94
004CFC86  movss    dword ptr [rip + 0x1b94e96], xmm3  ; -> 02064B24
004CFC8E  addss    xmm1, xmm6
004CFC92  mulss    xmm0, xmm2
004CFC96  movss    dword ptr [rip + 0x1b94e82], xmm6  ; -> 02064B20
004CFC9E  movss    dword ptr [rip + 0x1b94e82], xmm4  ; -> 02064B28
004CFCA6  addss    xmm0, xmm3
004CFCAA  movss    dword ptr [rip + 0x1b94e7a], xmm5  ; -> 02064B2C
004CFCB2  movss    xmm3, dword ptr [rip + 0x1b94ee2]  ; -> 02064B9C
004CFCBA  movss    dword ptr [rip + 0x1b94ffe], xmm1  ; -> 02064CC0
004CFCC2  movss    xmm1, dword ptr [rip + 0x1b94ece]  ; -> 02064B98
004CFCCA  mulss    xmm3, xmm2
004CFCCE  mulss    xmm1, xmm2
004CFCD2  addss    xmm3, xmm5
004CFCD6  movss    dword ptr [rip + 0x1b94fe6], xmm0  ; -> 02064CC4
004CFCDE  addss    xmm1, xmm4
004CFCE2  ucomiss  xmm3, xmm8
004CFCE6  movss    dword ptr [rip + 0x1b94fda], xmm1  ; -> 02064CC8
004CFCEE  movss    dword ptr [rip + 0x1b94fd6], xmm3  ; -> 02064CCC
004CFCF6  jp       0x4cfd00  ; -> 004CFD00
004CFCF8  jne      0x4cfd00  ; -> 004CFD00
004CFCFA  movaps   xmm0, xmm15
004CFCFE  jmp      0x4cfd07  ; -> 004CFD07
004CFD00  movaps   xmm0, xmm7
004CFD03  divss    xmm0, xmm3
004CFD07  movups   xmm1, xmmword ptr [rip + 0x1b94fb2]  ; -> 02064CC0
004CFD0E  movss    xmm4, dword ptr [rip + 0x1b94f9a]  ; -> 02064CB0
004CFD16  ucomiss  xmm11, xmm4
004CFD1A  movss    dword ptr [rip + 0x1b94dde], xmm0  ; -> 02064B00
004CFD22  shufps   xmm0, xmm0, 0
004CFD26  mulps    xmm1, xmm0
004CFD29  movups   xmmword ptr [rip + 0x1b94f90], xmm1  ; -> 02064CC0
004CFD30  jp       0x4cfd3c  ; -> 004CFD3C
004CFD32  jne      0x4cfd3c  ; -> 004CFD3C
004CFD34  mov      r9d, 1
004CFD3A  jmp      0x4cfd3f  ; -> 004CFD3F
004CFD3C  xor      r9d, r9d
004CFD3F  movss    xmm1, dword ptr [rip + 0x1b94f6d]  ; -> 02064CB4
004CFD47  ucomiss  xmm9, xmm1
004CFD4B  jp       0x4cfd56  ; -> 004CFD56
004CFD4D  jne      0x4cfd56  ; -> 004CFD56
004CFD4F  mov      edx, 1
004CFD54  jmp      0x4cfd58  ; -> 004CFD58
004CFD56  xor      edx, edx
004CFD58  movss    xmm0, dword ptr [rip + 0x1b94f58]  ; -> 02064CB8
004CFD60  ucomiss  xmm10, xmm0
004CFD64  jp       0x4cfd6f  ; -> 004CFD6F
004CFD66  jne      0x4cfd6f  ; -> 004CFD6F
004CFD68  mov      ecx, 1
004CFD6D  jmp      0x4cfd71  ; -> 004CFD71
004CFD6F  xor      ecx, ecx
004CFD71  movss    xmm5, dword ptr [rip + 0x1b94f47]  ; -> 02064CC0
004CFD79  xor      r8d, r8d
004CFD7C  comiss   xmm4, xmm11
004CFD80  seta     r8b
004CFD84  xor      eax, eax
004CFD86  add      r8w, r8w
004CFD8A  comiss   xmm1, xmm9
004CFD8E  seta     al
004CFD91  add      r8w, ax
004CFD95  xor      eax, eax
004CFD97  add      r8w, r8w
004CFD9B  comiss   xmm0, xmm10
004CFD9F  seta     al
004CFDA2  add      r8w, ax
004CFDA6  shl      r8w, 2
004CFDAB  add      r8w, r9w
004CFDAF  add      r8w, r8w
004CFDB3  add      r8w, dx
004CFDB7  add      r8w, r8w
004CFDBB  add      r8w, cx
004CFDBF  add      r8w, r8w
004CFDC3  ucomiss  xmm11, xmm5
004CFDC7  mov      word ptr [rip + 0x1b94d41], r8w  ; -> 02064B10
004CFDCF  jp       0x4cfddb  ; -> 004CFDDB
004CFDD1  jne      0x4cfddb  ; -> 004CFDDB
004CFDD3  mov      r10d, 1
004CFDD9  jmp      0x4cfdde  ; -> 004CFDDE
004CFDDB  xor      r10d, r10d
004CFDDE  movss    xmm2, dword ptr [rip + 0x1b94ede]  ; -> 02064CC4
004CFDE6  ucomiss  xmm9, xmm2
004CFDEA  jp       0x4cfdf5  ; -> 004CFDF5
004CFDEC  jne      0x4cfdf5  ; -> 004CFDF5
004CFDEE  mov      edx, 1
004CFDF3  jmp      0x4cfdf7  ; -> 004CFDF7
004CFDF5  xor      edx, edx
004CFDF7  movss    xmm3, dword ptr [rip + 0x1b94ec9]  ; -> 02064CC8
004CFDFF  ucomiss  xmm10, xmm3
004CFE03  jp       0x4cfe0e  ; -> 004CFE0E
004CFE05  jne      0x4cfe0e  ; -> 004CFE0E
004CFE07  mov      ecx, 1
004CFE0C  jmp      0x4cfe10  ; -> 004CFE10
004CFE0E  xor      ecx, ecx
004CFE10  xor      r9d, r9d
004CFE13  comiss   xmm5, xmm11
004CFE17  seta     r9b
004CFE1B  xor      eax, eax
004CFE1D  add      r9w, r9w
004CFE21  comiss   xmm2, xmm9
004CFE25  seta     al
004CFE28  add      r9w, ax
004CFE2C  xor      eax, eax
004CFE2E  add      r9w, r9w
004CFE32  comiss   xmm3, xmm10
004CFE36  seta     al
004CFE39  add      r9w, ax
004CFE3D  shl      r9w, 2
004CFE42  add      r9w, r10w
004CFE46  add      r9w, r9w
004CFE4A  add      r9w, dx
004CFE4E  add      r9w, r9w
004CFE52  add      r9w, cx
004CFE56  add      r9w, r9w
004CFE5A  ucomiss  xmm4, xmm14
004CFE5E  mov      word ptr [rip + 0x1b94cac], r9w  ; -> 02064B12
004CFE66  jp       0x4cfe72  ; -> 004CFE72
004CFE68  jne      0x4cfe72  ; -> 004CFE72
004CFE6A  mov      r11d, 1
004CFE70  jmp      0x4cfe75  ; -> 004CFE75
004CFE72  xor      r11d, r11d
004CFE75  ucomiss  xmm1, xmm12
004CFE79  jp       0x4cfe84  ; -> 004CFE84
004CFE7B  jne      0x4cfe84  ; -> 004CFE84
004CFE7D  mov      edx, 1
004CFE82  jmp      0x4cfe86  ; -> 004CFE86
004CFE84  xor      edx, edx
004CFE86  ucomiss  xmm0, xmm13
004CFE8A  jp       0x4cfe95  ; -> 004CFE95
004CFE8C  jne      0x4cfe95  ; -> 004CFE95
004CFE8E  mov      ecx, 1
004CFE93  jmp      0x4cfe97  ; -> 004CFE97
004CFE95  xor      ecx, ecx
004CFE97  xor      r10d, r10d
004CFE9A  comiss   xmm14, xmm4
004CFE9E  seta     r10b
004CFEA2  xor      eax, eax
004CFEA4  add      r10w, r10w
004CFEA8  comiss   xmm12, xmm1
004CFEAC  seta     al
004CFEAF  add      r10w, ax
004CFEB3  xor      eax, eax
004CFEB5  add      r10w, r10w
004CFEB9  comiss   xmm13, xmm0
004CFEBD  seta     al
004CFEC0  add      r10w, ax
004CFEC4  shl      r10w, 2
004CFEC9  add      r10w, r11w
004CFECD  add      r10w, r10w
004CFED1  add      r10w, dx
004CFED5  add      r10w, r10w
004CFED9  add      r10w, cx
004CFEDD  add      r10w, r10w
004CFEE1  ucomiss  xmm5, xmm14
004CFEE5  mov      word ptr [rip + 0x1b94c27], r10w  ; -> 02064B14
004CFEED  jp       0x4cfef8  ; -> 004CFEF8
004CFEEF  jne      0x4cfef8  ; -> 004CFEF8
004CFEF1  mov      ebx, 1
004CFEF6  jmp      0x4cfefa  ; -> 004CFEFA
004CFEF8  xor      ebx, ebx
004CFEFA  ucomiss  xmm2, xmm12
004CFEFE  jp       0x4cff0a  ; -> 004CFF0A
004CFF00  jne      0x4cff0a  ; -> 004CFF0A
004CFF02  mov      r11d, 1
004CFF08  jmp      0x4cff0d  ; -> 004CFF0D
004CFF0A  xor      r11d, r11d
004CFF0D  ucomiss  xmm3, xmm13
004CFF11  jp       0x4cff1c  ; -> 004CFF1C
004CFF13  jne      0x4cff1c  ; -> 004CFF1C
004CFF15  mov      ecx, 1
004CFF1A  jmp      0x4cff1e  ; -> 004CFF1E
004CFF1C  xor      ecx, ecx
004CFF1E  movsd    xmm0, qword ptr [rip + 0x1b94d8a]  ; -> 02064CB0
004CFF26  xor      edx, edx
004CFF28  comiss   xmm14, xmm5
004CFF2C  seta     dl
004CFF2F  xor      eax, eax
004CFF31  add      dx, dx
004CFF34  comiss   xmm12, xmm2
004CFF38  seta     al
004CFF3B  add      dx, ax
004CFF3E  xor      eax, eax
004CFF40  add      dx, dx
004CFF43  comiss   xmm13, xmm3
004CFF47  seta     al
004CFF4A  and      r10w, r12w
004CFF4E  add      dx, ax
004CFF51  mov      word ptr [rip + 0x1b94e87], r10w  ; -> 02064DE0
004CFF59  shl      dx, 2
004CFF5D  and      r8w, r12w
004CFF61  add      dx, bx
004CFF64  movsx    eax, r10w
004CFF68  or       r8w, ax
004CFF6C  lea      rbx, [rip + 0x1b94ebd]  ; -> 02064E30
004CFF73  movsd    qword ptr [rsi + rbx], xmm0
004CFF78  add      dx, dx
004CFF7B  add      dx, r11w
004CFF7F  mov      word ptr [rip + 0x1b94e51], r8w  ; -> 02064DD8
004CFF87  add      dx, dx
004CFF8A  and      r9w, r12w
004CFF8E  add      dx, cx
004CFF91  add      di, 2
004CFF95  add      dx, dx
004CFF98  mov      word ptr [rip + 0x1b94e29], di  ; -> 02064DC8
004CFF9F  movzx    ecx, r12w
004CFFA3  mov      word ptr [rip + 0x1b94b6c], dx  ; -> 02064B16
004CFFAA  and      cx, dx
004CFFAD  movaps   xmm0, xmm5
004CFFB0  movsx    eax, cx
004CFFB3  or       r9w, ax
004CFFB7  unpcklps xmm0, xmm2
004CFFBA  mov      eax, dword ptr [rip + 0x1b94cf8]  ; -> 02064CB8
004CFFC0  mov      dword ptr [rsi + rbx + 8], eax
004CFFC4  mov      eax, dword ptr [rip + 0x1b94cfe]  ; -> 02064CC8
004CFFCA  movsd    qword ptr [rbx + rbp], xmm0
004CFFCF  mov      dword ptr [rbx + rbp + 8], eax
004CFFD3  movzx    eax, r8w
004CFFD7  mov      dword ptr [rsi + rbx + 0xc], eax
004CFFDB  movzx    eax, r9w
004CFFDF  mov      dword ptr [rbx + rbp + 0xc], eax
004CFFE3  mov      word ptr [rip + 0x1b94dfa], cx  ; -> 02064DE4
004CFFEA  mov      word ptr [rip + 0x1b94dea], r9w  ; -> 02064DDC
004CFFF2  movsd    qword ptr [rip + 0x1b94cc6], xmm0  ; -> 02064CC0
004CFFFA  cmp      r14w, r15w
004CFFFE  jne      0x4cfa20  ; -> 004CFA20
004D0004  mov      rsi, qword ptr [rsp + 0x20]
004D0009  lea      rbp, [rip + 0x1b94e20]  ; -> 02064E30
004D0010  add      r15w, 0x10
004D0015  mov      word ptr [rip + 0x1b94da7], r14w  ; -> 02064DC4
004D001D  movsx    eax, r15w
004D0021  xor      r8d, r8d
004D0024  shl      eax, 4
004D0027  mov      rdx, rsi
004D002A  movsxd   rcx, eax
004D002D  add      rcx, rbp
004D0030  mov      word ptr [rip + 0x1b94d9c], r15w  ; -> 02064DD4
004D0038  call     r13
004D003B  movsx    r11d, word ptr [rip + 0x1b94ac9]  ; -> 02064B0C
004D0043  mov      r14d, 4
004D0049  mov      ebx, r11d
004D004C  add      bx, r11w
004D0050  mov      word ptr [rip + 0x1b94d71], bx  ; -> 02064DC8
004D0057  lea      edi, [r11 + 6]
004D005B  lea      r15d, [r14 + 4]
004D005F  lea      r12d, [r14 + 0xc]
004D0063  nop      dword ptr [rax]
004D0067  nop      word ptr [rax + rax]
004D0070  movsx    eax, bx
004D0073  dec      di
004D0076  add      eax, 0xa
004D0079  mov      word ptr [rip + 0x1b94d44], di  ; -> 02064DC4
004D0080  shl      eax, 4
004D0083  movsxd   rcx, eax
004D0086  movsx    r8d, word ptr [rcx + rbp + 0xc]
004D008C  movsx    eax, word ptr [rcx + rbp]
004D0090  add      eax, 0x64
004D0093  mov      word ptr [rip + 0x1b94d49], r8w  ; -> 02064DE4
004D009B  shl      eax, 4
004D009E  movsxd   r9, eax
004D00A1  movsx    eax, word ptr [rcx + rbp + 4]
004D00A6  add      eax, 0x64
004D00A9  shl      eax, 4
004D00AC  movups   xmm0, xmmword ptr [r9 + rbp]
004D00B1  movzx    r9d, word ptr [r9 + rbp + 0xc]
004D00B7  movsxd   r10, eax
004D00BA  movsx    eax, word ptr [rcx + rbp + 8]
004D00BF  add      eax, 0x64
004D00C2  shl      eax, 4
004D00C5  movsx    ecx, word ptr [r10 + rbp + 0xc]
004D00CB  movsxd   rdx, eax
004D00CE  lea      eax, [r8 + 0x64]
004D00D2  shl      eax, 4
004D00D5  movsxd   r8, eax
004D00D8  movups   xmmword ptr [rip + 0x1b94bd1], xmm0  ; -> 02064CB0
004D00DF  mov      word ptr [rip + 0x1b94cf2], cx  ; -> 02064DD8
004D00E6  movups   xmm0, xmmword ptr [r10 + rbp]
004D00EB  movsx    eax, word ptr [r8 + rbp + 0xc]
004D00F1  mov      word ptr [rip + 0x1b94ce8], ax  ; -> 02064DE0
004D00F8  movups   xmmword ptr [rip + 0x1b94bc1], xmm0  ; -> 02064CC0
004D00FF  movups   xmm0, xmmword ptr [rdx + rbp]
004D0103  movzx    edx, word ptr [rdx + rbp + 0xc]
004D0108  or       dx, ax
004D010B  movsx    eax, dx
004D010E  or       ax, cx
004D0111  mov      word ptr [rip + 0x1b94cc4], dx  ; -> 02064DDC
004D0118  or       r9w, ax
004D011C  mov      word ptr [rip + 0x1b94cb0], r9w  ; -> 02064DD4
004D0124  movups   xmmword ptr [rip + 0x1b94ba5], xmm0  ; -> 02064CD0
004D012B  movups   xmm0, xmmword ptr [r8 + rbp]
004D0130  movups   xmmword ptr [rip + 0x1b94ba9], xmm0  ; -> 02064CE0
004D0137  cmp      r9w, r11w
004D013B  jne      0x4d0418  ; -> 004D0418
004D0141  movss    xmm1, dword ptr [rip + 0x1b94b77]  ; -> 02064CC0
004D0149  subss    xmm1, dword ptr [rip + 0x1b94b5f]  ; -> 02064CB0
004D0151  movss    xmm0, dword ptr [rip + 0x1b94b6b]  ; -> 02064CC4
004D0159  subss    xmm0, dword ptr [rip + 0x1b94b53]  ; -> 02064CB4
004D0161  ucomiss  xmm1, xmm8
004D0165  movss    dword ptr [rip + 0x1b94b83], xmm1  ; -> 02064CF0
004D016D  movss    dword ptr [rip + 0x1b94b7f], xmm0  ; -> 02064CF4
004D0175  jp       0x4d0179  ; -> 004D0179
004D0177  je       0x4d0181  ; -> 004D0181
004D0179  ucomiss  xmm0, xmm8
004D017D  jp       0x4d0196  ; -> 004D0196
004D017F  jne      0x4d0196  ; -> 004D0196
004D0181  call     0x22cc40  ; -> 0022CC40 fn
004D0186  movss    xmm0, dword ptr [rip + 0x1b94b66]  ; -> 02064CF4
004D018E  movss    xmm1, dword ptr [rip + 0x1b94b5a]  ; -> 02064CF0
004D0196  comiss   xmm8, xmm1
004D019A  ja       0x4d01a2  ; -> 004D01A2
004D019C  comiss   xmm8, xmm0
004D01A0  jbe      0x4d01a7  ; -> 004D01A7
004D01A2  call     0x22cc30  ; -> 0022CC30 fn
004D01A7  call     0x22cc20  ; -> 0022CC20 fn
004D01AC  movss    xmm1, dword ptr [rip + 0x1b94b2c]  ; -> 02064CE0
004D01B4  subss    xmm1, dword ptr [rip + 0x1b94af4]  ; -> 02064CB0
004D01BC  movss    xmm0, dword ptr [rip + 0x1b94b20]  ; -> 02064CE4
004D01C4  subss    xmm0, dword ptr [rip + 0x1b94ae8]  ; -> 02064CB4
004D01CC  ucomiss  xmm1, xmm8
004D01D0  movss    dword ptr [rip + 0x1b94b28], xmm1  ; -> 02064D00
004D01D8  movss    dword ptr [rip + 0x1b94b24], xmm0  ; -> 02064D04
004D01E0  jp       0x4d01e4  ; -> 004D01E4
004D01E2  je       0x4d01ec  ; -> 004D01EC
004D01E4  ucomiss  xmm0, xmm8
004D01E8  jp       0x4d0201  ; -> 004D0201
004D01EA  jne      0x4d0201  ; -> 004D0201
004D01EC  call     0x22cc40  ; -> 0022CC40 fn
004D01F1  movss    xmm0, dword ptr [rip + 0x1b94b0b]  ; -> 02064D04
004D01F9  movss    xmm1, dword ptr [rip + 0x1b94aff]  ; -> 02064D00
004D0201  comiss   xmm8, xmm1
004D0205  ja       0x4d020d  ; -> 004D020D
004D0207  comiss   xmm8, xmm0
004D020B  jbe      0x4d0212  ; -> 004D0212
004D020D  call     0x22cc30  ; -> 0022CC30 fn
004D0212  call     0x22cc20  ; -> 0022CC20 fn
004D0217  movss    xmm5, dword ptr [rip + 0x1b94ad5]  ; -> 02064CF4
004D021F  movss    xmm1, dword ptr [rip + 0x1b94ad1]  ; -> 02064CF8
004D0227  movaps   xmm9, xmm5
004D022B  mulss    xmm9, dword ptr [rip + 0x1b94ad4]  ; -> 02064D08
004D0234  movaps   xmm6, xmm1
004D0237  movss    xmm4, dword ptr [rip + 0x1b94ab1]  ; -> 02064CF0
004D023F  mulss    xmm6, dword ptr [rip + 0x1b94ab9]  ; -> 02064D00
004D0247  movaps   xmm7, xmm4
004D024A  mulss    xmm7, dword ptr [rip + 0x1b94ab2]  ; -> 02064D04
004D0252  mulss    xmm1, dword ptr [rip + 0x1b94aaa]  ; -> 02064D04
004D025A  mulss    xmm4, dword ptr [rip + 0x1b94aa6]  ; -> 02064D08
004D0262  mulss    xmm5, dword ptr [rip + 0x1b94a96]  ; -> 02064D00
004D026A  movss    dword ptr [rip + 0x1b948ad], xmm9  ; -> 02064B20
004D0273  subss    xmm9, xmm1
004D0278  movss    dword ptr [rip + 0x1b948a4], xmm6  ; -> 02064B24
004D0280  subss    xmm6, xmm4
004D0284  movss    dword ptr [rip + 0x1b9489c], xmm7  ; -> 02064B28
004D028C  subss    xmm7, xmm5
004D0290  ucomiss  xmm9, xmm8
004D0294  jp       0x4d02a0  ; -> 004D02A0
004D0296  jne      0x4d02a0  ; -> 004D02A0
004D0298  mov      r9d, 1
004D029E  jmp      0x4d02a3  ; -> 004D02A3
004D02A0  xor      r9d, r9d
004D02A3  ucomiss  xmm6, xmm8
004D02A7  jp       0x4d02b3  ; -> 004D02B3
004D02A9  jne      0x4d02b3  ; -> 004D02B3
004D02AB  mov      r8d, 1
004D02B1  jmp      0x4d02b6  ; -> 004D02B6
004D02B3  xor      r8d, r8d
004D02B6  ucomiss  xmm7, xmm8
004D02BA  jp       0x4d02c5  ; -> 004D02C5
004D02BC  jne      0x4d02c5  ; -> 004D02C5
004D02BE  mov      edx, 1
004D02C3  jmp      0x4d02c7  ; -> 004D02C7
004D02C5  xor      edx, edx
004D02C7  movzx    r11d, word ptr [rip + 0x1b9483d]  ; -> 02064B0C
004D02CF  xor      ecx, ecx
004D02D1  comiss   xmm8, xmm7
004D02D5  cmova    cx, r14w
004D02DA  xor      eax, eax
004D02DC  comiss   xmm8, xmm6
004D02E0  cmova    ax, r15w
004D02E5  add      cx, ax
004D02E8  xor      eax, eax
004D02EA  comiss   xmm8, xmm9
004D02EE  cmova    ax, r12w
004D02F3  add      cx, ax
004D02F6  lea      eax, [r11 + 0x20]
004D02FA  add      cx, r9w
004D02FE  add      cx, cx
004D0301  add      cx, r8w
004D0305  add      cx, cx
004D0308  add      cx, dx
004D030B  add      cx, cx
004D030E  and      ax, cx
004D0311  mov      word ptr [rip + 0x1b947f8], cx  ; -> 02064B10
004D0318  mov      word ptr [rip + 0x1b94ab5], ax  ; -> 02064DD4
004D031F  cmp      ax, r11w
004D0323  je       0x4d040a  ; -> 004D040A
004D0329  movaps   xmm2, xmmword ptr [rip + 0x4450c0]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004D0330  movsx    edx, word ptr [rip + 0x1b94a7d]  ; -> 02064DB4
004D0337  movaps   xmm1, xmm2
004D033A  movups   xmm0, xmmword ptr [rip + 0x1b9496f]  ; -> 02064CB0
004D0341  inc      word ptr [rip + 0x1b94a70]  ; -> 02064DB8
004D0348  mov      eax, edx
004D034A  shl      eax, 4
004D034D  inc      dx
004D0350  movsxd   rcx, eax
004D0353  mulps    xmm1, xmm0
004D0356  movsx    eax, dx
004D0359  inc      dx
004D035C  movups   xmm0, xmmword ptr [rip + 0x1b9495d]  ; -> 02064CC0
004D0363  shl      eax, 4
004D0366  cvttps2dq xmm3, xmm1
004D036A  movaps   xmm1, xmm2
004D036D  mulps    xmm1, xmm0
004D0370  movups   xmm0, xmmword ptr [rip + 0x1b94959]  ; -> 02064CD0
004D0377  movups   xmmword ptr [rip + 0x1b94932], xmm3  ; -> 02064CB0
004D037E  cvttps2dq xmm4, xmm1
004D0382  movaps   xmm1, xmm2
004D0385  mulps    xmm1, xmm0
004D0388  movups   xmm0, xmmword ptr [rip + 0x1b94951]  ; -> 02064CE0
004D038F  movups   xmmword ptr [rip + 0x1b9492a], xmm4  ; -> 02064CC0
004D0396  cvttps2dq xmm5, xmm1
004D039A  mulps    xmm2, xmm0
004D039D  movups   xmm0, xmmword ptr [rip + 0x1b947fc]  ; -> 02064BA0
004D03A4  movups   xmmword ptr [rip + 0x1b94925], xmm5  ; -> 02064CD0
004D03AB  movups   xmmword ptr [rcx + rbp], xmm0
004D03AF  movsxd   rcx, eax
004D03B2  movsx    eax, dx
004D03B5  inc      dx
004D03B8  shl      eax, 4
004D03BB  cvttps2dq xmm1, xmm2
004D03BF  movups   xmmword ptr [rcx + rbp], xmm3
004D03C3  movsxd   rcx, eax
004D03C6  movsx    eax, dx
004D03C9  inc      dx
004D03CC  shl      eax, 4
004D03CF  movups   xmmword ptr [rip + 0x1b9490a], xmm1  ; -> 02064CE0
004D03D6  movups   xmmword ptr [rcx + rbp], xmm4
004D03DA  movsxd   rcx, eax
004D03DD  movsx    eax, dx
004D03E0  inc      dx
004D03E3  shl      eax, 4
004D03E6  cdqe     
004D03E8  movups   xmmword ptr [rcx + rbp], xmm5
004D03EC  mov      word ptr [rip + 0x1b949c1], dx  ; -> 02064DB4
004D03F3  mov      rcx, r13
004D03F6  mov      rdx, rsi
004D03F9  movups   xmmword ptr [rax + rbp], xmm1
004D03FD  call     0x4cf3b0  ; -> 004CF3B0 fn
004D0402  movzx    r11d, word ptr [rip + 0x1b94702]  ; -> 02064B0C
004D040A  movzx    ebx, word ptr [rip + 0x1b949b7]  ; -> 02064DC8
004D0411  movzx    edi, word ptr [rip + 0x1b949ac]  ; -> 02064DC4
004D0418  inc      bx
004D041B  mov      word ptr [rip + 0x1b949a6], bx  ; -> 02064DC8
004D0422  cmp      di, r11w
004D0426  jne      0x4d0070  ; -> 004D0070
004D042C  add      r11w, 0x13
004D0431  xor      r8d, r8d
004D0434  movsx    eax, r11w
004D0438  mov      rdx, rsi
004D043B  shl      eax, 4
004D043E  movsxd   rcx, eax
004D0441  add      rcx, rbp
004D0444  mov      word ptr [rip + 0x1b94988], r11w  ; -> 02064DD4
004D044C  call     r13
004D044F  movsx    ebx, word ptr [rip + 0x1b946b6]  ; -> 02064B0C
004D0456  mov      r11d, ebx
004D0459  add      r11w, bx
004D045D  mov      word ptr [rip + 0x1b94963], r11w  ; -> 02064DC8
004D0465  lea      edi, [rbx + 6]
004D0468  nop      dword ptr [rax + rax]
004D0470  movsx    eax, r11w
004D0474  dec      di
004D0477  add      eax, 0xa
004D047A  mov      word ptr [rip + 0x1b94943], di  ; -> 02064DC4
004D0481  shl      eax, 4
004D0484  movsxd   rcx, eax
004D0487  movsx    r8d, word ptr [rcx + rbp + 0xc]
004D048D  movsx    eax, word ptr [rcx + rbp]
004D0491  add      eax, 0x64
004D0494  mov      word ptr [rip + 0x1b94948], r8w  ; -> 02064DE4
004D049C  shl      eax, 4
004D049F  movsxd   r9, eax
004D04A2  movsx    eax, word ptr [rcx + rbp + 4]
004D04A7  add      eax, 0x64
004D04AA  shl      eax, 4
004D04AD  movups   xmm0, xmmword ptr [r9 + rbp]
004D04B2  movzx    r9d, word ptr [r9 + rbp + 0xc]
004D04B8  movsxd   r10, eax
004D04BB  movsx    eax, word ptr [rcx + rbp + 8]
004D04C0  add      eax, 0x64
004D04C3  shl      eax, 4
004D04C6  movsx    ecx, word ptr [r10 + rbp + 0xc]
004D04CC  movsxd   rdx, eax
004D04CF  lea      eax, [r8 + 0x64]
004D04D3  shl      eax, 4
004D04D6  movsxd   r8, eax
004D04D9  movups   xmmword ptr [rip + 0x1b947d0], xmm0  ; -> 02064CB0
004D04E0  mov      word ptr [rip + 0x1b948f1], cx  ; -> 02064DD8
004D04E7  movups   xmm0, xmmword ptr [r10 + rbp]
004D04EC  movsx    eax, word ptr [r8 + rbp + 0xc]
004D04F2  mov      word ptr [rip + 0x1b948e7], ax  ; -> 02064DE0
004D04F9  movups   xmmword ptr [rip + 0x1b947c0], xmm0  ; -> 02064CC0
004D0500  movups   xmm0, xmmword ptr [rdx + rbp]
004D0504  movzx    edx, word ptr [rdx + rbp + 0xc]
004D0509  or       dx, ax
004D050C  movsx    eax, dx
004D050F  or       ax, cx
004D0512  mov      word ptr [rip + 0x1b948c3], dx  ; -> 02064DDC
004D0519  or       r9w, ax
004D051D  mov      word ptr [rip + 0x1b948af], r9w  ; -> 02064DD4
004D0525  movups   xmmword ptr [rip + 0x1b947a4], xmm0  ; -> 02064CD0
004D052C  movups   xmm0, xmmword ptr [r8 + rbp]
004D0531  movups   xmmword ptr [rip + 0x1b947a8], xmm0  ; -> 02064CE0
004D0538  cmp      r9w, bx
004D053C  jne      0x4d0816  ; -> 004D0816
004D0542  movss    xmm1, dword ptr [rip + 0x1b94776]  ; -> 02064CC0
004D054A  subss    xmm1, dword ptr [rip + 0x1b9475e]  ; -> 02064CB0
004D0552  movss    xmm0, dword ptr [rip + 0x1b9476a]  ; -> 02064CC4
004D055A  subss    xmm0, dword ptr [rip + 0x1b94752]  ; -> 02064CB4
004D0562  ucomiss  xmm1, xmm8
004D0566  movss    dword ptr [rip + 0x1b94782], xmm1  ; -> 02064CF0
004D056E  movss    dword ptr [rip + 0x1b9477e], xmm0  ; -> 02064CF4
004D0576  jp       0x4d057a  ; -> 004D057A
004D0578  je       0x4d0582  ; -> 004D0582
004D057A  ucomiss  xmm0, xmm8
004D057E  jp       0x4d0597  ; -> 004D0597
004D0580  jne      0x4d0597  ; -> 004D0597
004D0582  call     0x22cc40  ; -> 0022CC40 fn
004D0587  movss    xmm0, dword ptr [rip + 0x1b94765]  ; -> 02064CF4
004D058F  movss    xmm1, dword ptr [rip + 0x1b94759]  ; -> 02064CF0
004D0597  comiss   xmm8, xmm1
004D059B  ja       0x4d05a3  ; -> 004D05A3
004D059D  comiss   xmm8, xmm0
004D05A1  jbe      0x4d05a8  ; -> 004D05A8
004D05A3  call     0x22cc30  ; -> 0022CC30 fn
004D05A8  call     0x22cc20  ; -> 0022CC20 fn
004D05AD  movss    xmm1, dword ptr [rip + 0x1b9472b]  ; -> 02064CE0
004D05B5  subss    xmm1, dword ptr [rip + 0x1b946f3]  ; -> 02064CB0
004D05BD  movss    xmm0, dword ptr [rip + 0x1b9471f]  ; -> 02064CE4
004D05C5  subss    xmm0, dword ptr [rip + 0x1b946e7]  ; -> 02064CB4
004D05CD  ucomiss  xmm1, xmm8
004D05D1  movss    dword ptr [rip + 0x1b94727], xmm1  ; -> 02064D00
004D05D9  movss    dword ptr [rip + 0x1b94723], xmm0  ; -> 02064D04
004D05E1  jp       0x4d05e5  ; -> 004D05E5
004D05E3  je       0x4d05ed  ; -> 004D05ED
004D05E5  ucomiss  xmm0, xmm8
004D05E9  jp       0x4d0602  ; -> 004D0602
004D05EB  jne      0x4d0602  ; -> 004D0602
004D05ED  call     0x22cc40  ; -> 0022CC40 fn
004D05F2  movss    xmm0, dword ptr [rip + 0x1b9470a]  ; -> 02064D04
004D05FA  movss    xmm1, dword ptr [rip + 0x1b946fe]  ; -> 02064D00
004D0602  comiss   xmm8, xmm1
004D0606  ja       0x4d060e  ; -> 004D060E
004D0608  comiss   xmm8, xmm0
004D060C  jbe      0x4d0613  ; -> 004D0613
004D060E  call     0x22cc30  ; -> 0022CC30 fn
004D0613  call     0x22cc20  ; -> 0022CC20 fn
004D0618  movss    xmm5, dword ptr [rip + 0x1b946d4]  ; -> 02064CF4
004D0620  movss    xmm1, dword ptr [rip + 0x1b946d0]  ; -> 02064CF8
004D0628  movaps   xmm9, xmm5
004D062C  mulss    xmm9, dword ptr [rip + 0x1b946d3]  ; -> 02064D08
004D0635  movaps   xmm6, xmm1
004D0638  movss    xmm4, dword ptr [rip + 0x1b946b0]  ; -> 02064CF0
004D0640  mulss    xmm6, dword ptr [rip + 0x1b946b8]  ; -> 02064D00
004D0648  movaps   xmm7, xmm4
004D064B  mulss    xmm7, dword ptr [rip + 0x1b946b1]  ; -> 02064D04
004D0653  mulss    xmm1, dword ptr [rip + 0x1b946a9]  ; -> 02064D04
004D065B  mulss    xmm4, dword ptr [rip + 0x1b946a5]  ; -> 02064D08
004D0663  mulss    xmm5, dword ptr [rip + 0x1b94695]  ; -> 02064D00
004D066B  movss    dword ptr [rip + 0x1b944ac], xmm9  ; -> 02064B20
004D0674  subss    xmm9, xmm1
004D0679  movss    dword ptr [rip + 0x1b944a3], xmm6  ; -> 02064B24
004D0681  subss    xmm6, xmm4
004D0685  movss    dword ptr [rip + 0x1b9449b], xmm7  ; -> 02064B28
004D068D  subss    xmm7, xmm5
004D0691  ucomiss  xmm9, xmm8
004D0695  jp       0x4d06a1  ; -> 004D06A1
004D0697  jne      0x4d06a1  ; -> 004D06A1
004D0699  mov      r9d, 1
004D069F  jmp      0x4d06a4  ; -> 004D06A4
004D06A1  xor      r9d, r9d
004D06A4  ucomiss  xmm6, xmm8
004D06A8  jp       0x4d06b4  ; -> 004D06B4
004D06AA  jne      0x4d06b4  ; -> 004D06B4
004D06AC  mov      r8d, 1
004D06B2  jmp      0x4d06b7  ; -> 004D06B7
004D06B4  xor      r8d, r8d
004D06B7  ucomiss  xmm7, xmm8
004D06BB  jp       0x4d06c6  ; -> 004D06C6
004D06BD  jne      0x4d06c6  ; -> 004D06C6
004D06BF  mov      edx, 1
004D06C4  jmp      0x4d06c8  ; -> 004D06C8
004D06C6  xor      edx, edx
004D06C8  movzx    ebx, word ptr [rip + 0x1b9443d]  ; -> 02064B0C
004D06CF  xor      ecx, ecx
004D06D1  comiss   xmm8, xmm7
004D06D5  cmova    cx, r14w
004D06DA  xor      eax, eax
004D06DC  comiss   xmm8, xmm6
004D06E0  cmova    ax, r15w
004D06E5  add      cx, ax
004D06E8  xor      eax, eax
004D06EA  comiss   xmm8, xmm9
004D06EE  cmova    ax, r12w
004D06F3  add      cx, ax
004D06F6  lea      eax, [rbx + 0x20]
004D06F9  add      cx, r9w
004D06FD  add      cx, cx
004D0700  add      cx, r8w
004D0704  add      cx, cx
004D0707  add      cx, dx
004D070A  add      cx, cx
004D070D  and      ax, cx
004D0710  mov      word ptr [rip + 0x1b943f9], cx  ; -> 02064B10
004D0717  mov      word ptr [rip + 0x1b946b6], ax  ; -> 02064DD4
004D071E  cmp      ax, bx
004D0721  jne      0x4d0807  ; -> 004D0807
004D0727  movaps   xmm2, xmmword ptr [rip + 0x444cc2]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004D072E  movsx    edx, word ptr [rip + 0x1b9467f]  ; -> 02064DB4
004D0735  movaps   xmm1, xmm2
004D0738  movups   xmm0, xmmword ptr [rip + 0x1b94571]  ; -> 02064CB0
004D073F  inc      word ptr [rip + 0x1b94672]  ; -> 02064DB8
004D0746  mov      eax, edx
004D0748  shl      eax, 4
004D074B  inc      dx
004D074E  movsxd   rcx, eax
004D0751  mulps    xmm1, xmm0
004D0754  movsx    eax, dx
004D0757  inc      dx
004D075A  movups   xmm0, xmmword ptr [rip + 0x1b9455f]  ; -> 02064CC0
004D0761  shl      eax, 4
004D0764  cvttps2dq xmm3, xmm1
004D0768  movaps   xmm1, xmm2
004D076B  mulps    xmm1, xmm0
004D076E  movups   xmm0, xmmword ptr [rip + 0x1b9455b]  ; -> 02064CD0
004D0775  movups   xmmword ptr [rip + 0x1b94534], xmm3  ; -> 02064CB0
004D077C  cvttps2dq xmm4, xmm1
004D0780  movaps   xmm1, xmm2
004D0783  mulps    xmm1, xmm0
004D0786  movups   xmm0, xmmword ptr [rip + 0x1b94553]  ; -> 02064CE0
004D078D  movups   xmmword ptr [rip + 0x1b9452c], xmm4  ; -> 02064CC0
004D0794  cvttps2dq xmm5, xmm1
004D0798  mulps    xmm2, xmm0
004D079B  movups   xmm0, xmmword ptr [rip + 0x1b9440e]  ; -> 02064BB0
004D07A2  movups   xmmword ptr [rip + 0x1b94527], xmm5  ; -> 02064CD0
004D07A9  movups   xmmword ptr [rcx + rbp], xmm0
004D07AD  movsxd   rcx, eax
004D07B0  movsx    eax, dx
004D07B3  inc      dx
004D07B6  shl      eax, 4
004D07B9  cvttps2dq xmm1, xmm2
004D07BD  movups   xmmword ptr [rcx + rbp], xmm3
004D07C1  movsxd   rcx, eax
004D07C4  movsx    eax, dx
004D07C7  inc      dx
004D07CA  shl      eax, 4
004D07CD  movups   xmmword ptr [rip + 0x1b9450c], xmm1  ; -> 02064CE0
004D07D4  movups   xmmword ptr [rcx + rbp], xmm4
004D07D8  movsxd   rcx, eax
004D07DB  movsx    eax, dx
004D07DE  inc      dx
004D07E1  shl      eax, 4
004D07E4  cdqe     
004D07E6  movups   xmmword ptr [rcx + rbp], xmm5
004D07EA  mov      word ptr [rip + 0x1b945c3], dx  ; -> 02064DB4
004D07F1  mov      rcx, r13
004D07F4  mov      rdx, rsi
004D07F7  movups   xmmword ptr [rax + rbp], xmm1
004D07FB  call     0x4cf3b0  ; -> 004CF3B0 fn
004D0800  movzx    ebx, word ptr [rip + 0x1b94305]  ; -> 02064B0C
004D0807  movzx    r11d, word ptr [rip + 0x1b945b9]  ; -> 02064DC8
004D080F  movzx    edi, word ptr [rip + 0x1b945ae]  ; -> 02064DC4
004D0816  inc      r11w
004D081A  mov      word ptr [rip + 0x1b945a6], r11w  ; -> 02064DC8
004D0822  cmp      di, bx
004D0825  jne      0x4d0470  ; -> 004D0470
004D082B  movaps   xmm14, xmmword ptr [rsp + 0x40]
004D0831  lea      r11, [rsp + 0xd0]
004D0839  mov      rbx, qword ptr [r11 + 0x50]
004D083D  movaps   xmm6, xmmword ptr [r11 - 0x10]
004D0842  movaps   xmm7, xmmword ptr [r11 - 0x20]
004D0847  movaps   xmm8, xmmword ptr [r11 - 0x30]
004D084C  movaps   xmm9, xmmword ptr [r11 - 0x40]
004D0851  movaps   xmm10, xmmword ptr [r11 - 0x50]
004D0856  movaps   xmm11, xmmword ptr [r11 - 0x60]
004D085B  movaps   xmm12, xmmword ptr [r11 - 0x70]
004D0860  movaps   xmm13, xmmword ptr [r11 - 0x80]
004D0865  movaps   xmm15, xmmword ptr [rsp + 0x30]
004D086B  mov      rsp, r11
004D086E  pop      r15
004D0870  pop      r14
004D0872  pop      r13
004D0874  pop      r12
004D0876  pop      rdi
004D0877  pop      rsi
004D0878  pop      rbp
004D0879  ret      
```

## 00524A10 (55 B, extent 00524A10-00524A47)

Page context: "same 177 B shape), walk '00463460' 2216 B | same walk family as '0xA2' | | '0xA3' | sub-step '00524800' 527 B (own '0020E600'/'0020E620' fixups + '002F31C0'), sub-walk '00524A50' 462 B | sub-seventh '00524A10' resolves '+0x294' | | '0xA4' | sub-step '005222D0' 43 B, sub-walk '00522300' 1268 B | setup to '+0x390' | | '0xA6'/'0xA8'/'0xAB' | sub-steps '00524D70'/'00527110'/'0052BFB0' (177 B '003D8E50'-shape), sub-setups '0054EED0'/'0054F35"

```
00524A10  push     rbx
00524A12  sub      rsp, 0x20
00524A16  mov      rbx, rcx
00524A19  mov      ecx, dword ptr [rcx + 0x294]
00524A1F  call     0x20e600  ; -> 0020E600 fn
00524A24  test     rax, rax
00524A27  je       0x524a41  ; -> 00524A41
00524A29  mov      ecx, dword ptr [rbx + 0x294]
00524A2F  call     0x20e600  ; -> 0020E600 fn
00524A34  mov      rcx, rax
00524A37  add      rsp, 0x20
00524A3B  pop      rbx
00524A3C  jmp      0x24b1c0  ; -> 0024B1C0 fn
00524A41  add      rsp, 0x20
00524A45  pop      rbx
00524A46  ret      
```
