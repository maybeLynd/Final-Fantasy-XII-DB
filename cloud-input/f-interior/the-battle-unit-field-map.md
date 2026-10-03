# F-interior pack: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-battle-unit-field-map.json`.

Functions: 19. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 27e0a8f0b	FABLE: GR-8 page corrections - scratch block 2.5 (+0x10 is not the previewed id; readers of +0x00/+0; 2e935e586	SWE2-DATA: published answers incorporated - section 18's binding-record cells corrected (SD-122 / SD; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 0022D4B0 (815 B, extent 0022D4B0-0022D7DF)

Page context: "E2-EC7-108 update (2026-09-20) - '002315E0' measured  '002315E0' (176 B) is the '0022F430' descriptor post '00318CA0' and '0032A4D0' call: null 'rcx' or '[rcx]' answers '0xFFFF'; otherwise it stages '0022D4B0' as the callback, copies the caller's two 16-byte blocks ('rdx' and 'r8') into the frame, seeds 'word = 0xFFFF' and 'dword = 0', runs '0022F430(&desc)' and returns the signed 'word[+0x44]' out field - the sibling post to '00232490'"

```
0022D4B0  mov      r11, rsp
0022D4B3  push     rdi
0022D4B4  push     r12
0022D4B6  push     r14
0022D4B8  push     r15
0022D4BA  sub      rsp, 0x88
0022D4C1  mov      rax, qword ptr [rip + 0x1d17368]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0022D4C8  xor      rax, rsp
0022D4CB  mov      qword ptr [rsp + 0x40], rax
0022D4D0  xor      r12d, r12d
0022D4D3  mov      rdi, rdx
0022D4D6  mov      r15, rcx
0022D4D9  mov      r14d, r12d
0022D4DC  cmp      r12w, word ptr [rdx + 0x40]
0022D4E1  jge      0x22d7c3  ; -> 0022D7C3
0022D4E7  mov      qword ptr [r11 - 0x28], rbp
0022D4EB  lea      r9, [rip + 0x1e6cdde]  ; -> 0209A2D0
0022D4F2  mov      qword ptr [r11 - 0x30], rsi
0022D4F6  lea      ebp, [r12 + 2]
0022D4FB  mov      qword ptr [r11 - 0x38], r13
0022D4FF  mov      edx, 0x4000
0022D504  movaps   xmmword ptr [rsp + 0x50], xmm7
0022D509  lea      r13d, [r12 + 1]
0022D50E  mov      qword ptr [r11 + 0x18], rbx
0022D512  mov      r8d, 0x5000
0022D518  movaps   xmmword ptr [rsp + 0x60], xmm6
0022D51D  xorps    xmm7, xmm7
0022D520  movsx    eax, word ptr [rdi + 0x3e]
0022D524  add      eax, r14d
0022D527  movsxd   rcx, eax
0022D52A  mov      rax, qword ptr [r15 + 0x28]
0022D52E  movzx    esi, word ptr [rax + rcx*2]
0022D532  cmp      si, r8w
0022D536  jge      0x22d78f  ; -> 0022D78F
0022D53C  cmp      si, dx
0022D53F  jl       0x22d616  ; -> 0022D616
0022D545  movsx    eax, si
0022D548  sub      eax, edx
0022D54A  cdqe     
0022D54C  lea      r10, [rax + rax*8]
0022D550  shl      r10, 4
0022D554  add      r10, qword ptr [r15 + 0x18]
0022D558  mov      ecx, dword ptr [r10 + 4]
0022D55C  shr      ecx, 0xd
0022D55F  and      ecx, 0x1f
0022D562  add      ecx, 0x20
0022D565  mov      edx, dword ptr [r9 + rcx*8 + 0x110]
0022D56D  mov      ebx, dword ptr [r9 + rcx*8 + 0x114]
0022D575  movzx    ecx, word ptr [rdi + 0x46]
0022D579  and      ebx, edx
0022D57B  not      edx
0022D57D  and      edx, dword ptr [r10 + 4]
0022D581  or       ebx, edx
0022D583  mov      eax, ebx
0022D585  and      eax, 7
0022D588  je       0x22d5c2  ; -> 0022D5C2
0022D58A  sub      eax, r13d
0022D58D  je       0x22d5a6  ; -> 0022D5A6
0022D58F  cmp      eax, 3
0022D592  jne      0x22d78a  ; -> 0022D78A
0022D598  cmp      cx, 4
0022D59C  mov      eax, r12d
0022D59F  sete     al
0022D5A2  test     eax, eax
0022D5A4  jmp      0x22d5bc  ; -> 0022D5BC
0022D5A6  cmp      ebx, 0x80000000
0022D5AC  jae      0x22d78a  ; -> 0022D78A
0022D5B2  bt       ebx, 0x1e
0022D5B6  jae      0x22d5c2  ; -> 0022D5C2
0022D5B8  cmp      cx, 4
0022D5BC  je       0x22d78a  ; -> 0022D78A
0022D5C2  mov      r9, qword ptr [rdi + 0x18]
0022D5C6  lea      rcx, [rsp + 0x30]
0022D5CB  mov      r8, qword ptr [rdi + 0x10]
0022D5CF  mov      rdx, r10
0022D5D2  call     0x380fa0  ; -> 00380FA0 fn
0022D5D7  comiss   xmm0, xmm7
0022D5DA  jb       0x22d77d  ; -> 0022D77D
0022D5E0  movss    xmm1, dword ptr [rdi + 0x30]
0022D5E5  comiss   xmm1, xmm0
0022D5E8  jbe      0x22d77d  ; -> 0022D77D
0022D5EE  bt       ebx, 0x17
0022D5F2  jb       0x22d74e  ; -> 0022D74E
0022D5F8  movss    dword ptr [rdi + 0x30], xmm0
0022D5FD  mov      rax, qword ptr [rdi + 0x20]
0022D601  movaps   xmm0, xmmword ptr [rsp + 0x30]
0022D606  movups   xmmword ptr [rax], xmm0
0022D609  mov      word ptr [rdi + 0x42], si
0022D60D  mov      word ptr [rdi + 0x44], bp
0022D611  jmp      0x22d77d  ; -> 0022D77D
0022D616  movsx    r8, si
0022D61A  shl      r8, 5
0022D61E  add      r8, qword ptr [r15 + 0x10]
0022D622  mov      ecx, dword ptr [r8 + 0xc]
0022D626  shr      ecx, 0xd
0022D629  and      ecx, 0x1f
0022D62C  add      ecx, 0x20
0022D62F  mov      edx, ecx
0022D631  mov      ecx, dword ptr [r9 + rcx*8 + 0x110]
0022D639  mov      ebx, ecx
0022D63B  mov      eax, dword ptr [r9 + rdx*8 + 0x114]
0022D643  not      ebx
0022D645  and      ebx, dword ptr [r8 + 0xc]
0022D649  and      eax, ecx
0022D64B  movzx    ecx, word ptr [rdi + 0x46]
0022D64F  or       ebx, eax
0022D651  mov      eax, ebx
0022D653  and      eax, 7
0022D656  je       0x22d690  ; -> 0022D690
0022D658  sub      eax, r13d
0022D65B  je       0x22d674  ; -> 0022D674
0022D65D  cmp      eax, 3
0022D660  jne      0x22d784  ; -> 0022D784
0022D666  cmp      cx, 4
0022D66A  mov      eax, r12d
0022D66D  sete     al
0022D670  test     eax, eax
0022D672  jmp      0x22d68a  ; -> 0022D68A
0022D674  cmp      ebx, 0x80000000
0022D67A  jae      0x22d784  ; -> 0022D784
0022D680  bt       ebx, 0x1e
0022D684  jae      0x22d690  ; -> 0022D690
0022D686  cmp      cx, 4
0022D68A  je       0x22d784  ; -> 0022D784
0022D690  movsx    rax, word ptr [r8 + 0x10]
0022D695  mov      rdx, rdi
0022D698  mov      rbp, qword ptr [rdi + 0x10]
0022D69C  shl      rax, 4
0022D6A0  mov      rcx, rbp
0022D6A3  add      rax, qword ptr [r15 + 8]
0022D6A7  mov      qword ptr [rsp + 0x20], r8
0022D6AC  lea      r8, [rsp + 0x20]
0022D6B1  mov      qword ptr [rsp + 0x28], rax
0022D6B6  call     0x22e6d0  ; -> 0022E6D0 fn
0022D6BB  movaps   xmm6, xmm0
0022D6BE  comiss   xmm6, xmm7
0022D6C1  jb       0x22d778  ; -> 0022D778
0022D6C7  movss    xmm1, dword ptr [rdi + 0x30]
0022D6CC  comiss   xmm1, xmm6
0022D6CF  jbe      0x22d778  ; -> 0022D778
0022D6D5  movaps   xmm3, xmm0
0022D6D8  lea      r8, [rsp + 0x30]
0022D6DD  divss    xmm3, dword ptr [rdi + 0x34]
0022D6E2  movzx    edx, si
0022D6E5  mov      rcx, r15
0022D6E8  movss    xmm0, dword ptr [rdi + 0xc]
0022D6ED  movaps   xmm2, xmm3
0022D6F0  movss    dword ptr [rsp + 0x3c], xmm0
0022D6F6  mulss    xmm2, dword ptr [rdi]
0022D6FA  movaps   xmm1, xmm3
0022D6FD  mulss    xmm1, dword ptr [rdi + 4]
0022D702  mulss    xmm3, dword ptr [rdi + 8]
0022D707  movss    dword ptr [rsp + 0x30], xmm2
0022D70D  movss    dword ptr [rsp + 0x34], xmm1
0022D713  movss    dword ptr [rsp + 0x38], xmm3
0022D719  addss    xmm2, dword ptr [rbp]
0022D71E  movss    dword ptr [rsp + 0x30], xmm2
0022D724  addss    xmm1, dword ptr [rbp + 4]
0022D729  movss    dword ptr [rsp + 0x34], xmm1
0022D72F  addss    xmm3, dword ptr [rbp + 8]
0022D734  movss    dword ptr [rsp + 0x38], xmm3
0022D73A  call     0x22cf50  ; -> 0022CF50 fn
0022D73F  test     eax, eax
0022D741  je       0x22d778  ; -> 0022D778
0022D743  mov      ebp, 2
0022D748  bt       ebx, 0x17
0022D74C  jae      0x22d76e  ; -> 0022D76E
0022D74E  lea      r9, [rip + 0x1e6cb7b]  ; -> 0209A2D0
0022D755  mov      edx, 0x4000
0022D75A  mov      r8d, 0x5000
0022D760  cmp      word ptr [rdi + 0x44], r12w
0022D765  jne      0x22d78f  ; -> 0022D78F
0022D767  mov      word ptr [rdi + 0x44], r13w
0022D76C  jmp      0x22d78f  ; -> 0022D78F
0022D76E  movss    dword ptr [rdi + 0x30], xmm6
0022D773  jmp      0x22d5fd  ; -> 0022D5FD
0022D778  mov      ebp, 2
0022D77D  lea      r9, [rip + 0x1e6cb4c]  ; -> 0209A2D0
0022D784  mov      r8d, 0x5000
0022D78A  mov      edx, 0x4000
0022D78F  movsx    eax, word ptr [rdi + 0x40]
0022D793  inc      r14d
0022D796  cmp      r14d, eax
0022D799  jl       0x22d520  ; -> 0022D520
0022D79F  movaps   xmm7, xmmword ptr [rsp + 0x50]
0022D7A4  movaps   xmm6, xmmword ptr [rsp + 0x60]
0022D7A9  mov      r13, qword ptr [rsp + 0x70]
0022D7AE  mov      rsi, qword ptr [rsp + 0x78]
0022D7B3  mov      rbp, qword ptr [rsp + 0x80]
0022D7BB  mov      rbx, qword ptr [rsp + 0xc0]
0022D7C3  mov      rcx, qword ptr [rsp + 0x40]
0022D7C8  xor      rcx, rsp
0022D7CB  call     0x808c40  ; -> 00808C40 fn
0022D7D0  add      rsp, 0x88
0022D7D7  pop      r15
0022D7D9  pop      r14
0022D7DB  pop      r12
0022D7DD  pop      rdi
0022D7DE  ret      
```

## 00234A10 (99 B, extent 00234A10-00234A73)

Page context: "14E') | 'BattleUnit_RecoverFromTerminalStatusSetIfClear' '00301140' ('00301295'); 'BattleUnit_ResetStateForReuse' '00236A60' ('00236AA6') |  | | 11 | '0x800' | 'SpawnGroup_SetUnitFlag800ByGroupMask' '00234A10' — the verb 'hideenemy' '0479' | 'SpawnGroup_ClearUnitFlag800ByGroupMask' '00234A80' — the verb 'showenemy' '0478'; 'BattleUnit_ResetStateForReuse' '00236A60' ('00236AA6') | 'BattleUnit_ComputePresentationSuppressionMask' '003125E0"

```
00234A10  mov      qword ptr [rsp + 8], rbx
00234A15  push     rdi
00234A16  sub      rsp, 0x20
00234A1A  xor      ebx, ebx
00234A1C  mov      edi, ecx
00234A1E  cmp      dword ptr [rip + 0x1e59c7c], ebx  ; -> 0208E6A0
00234A24  jle      0x234a68  ; -> 00234A68
00234A26  mov      ecx, ebx
00234A28  call     0x321170  ; -> 00321170 fn
00234A2D  test     rax, rax
00234A30  je       0x234a5e  ; -> 00234A5E
00234A32  mov      rcx, qword ptr [rax + 0x698]
00234A39  test     rcx, rcx
00234A3C  je       0x234a5e  ; -> 00234A5E
00234A3E  cmp      byte ptr [rcx + 5], 1
00234A42  jne      0x234a5e  ; -> 00234A5E
00234A44  movzx    ecx, byte ptr [rax + 0xe98]
00234A4B  bt       edi, ecx
00234A4E  jae      0x234a5e  ; -> 00234A5E
00234A50  or       dword ptr [rax], 0x800
00234A56  mov      rcx, rax
00234A59  call     0x312700  ; -> 00312700 fn
00234A5E  inc      ebx
00234A60  cmp      ebx, dword ptr [rip + 0x1e59c3a]  ; -> 0208E6A0
00234A66  jl       0x234a26  ; -> 00234A26
00234A68  mov      rbx, qword ptr [rsp + 0x30]
00234A6D  add      rsp, 0x20
00234A71  pop      rdi
00234A72  ret      
```

## 00234A80 (99 B, extent 00234A80-00234AE3)

Page context: "attleUnit_ResetStateForReuse' '00236A60' ('00236AA6') |  | | 11 | '0x800' | 'SpawnGroup_SetUnitFlag800ByGroupMask' '00234A10' — the verb 'hideenemy' '0479' | 'SpawnGroup_ClearUnitFlag800ByGroupMask' '00234A80' — the verb 'showenemy' '0478'; 'BattleUnit_ResetStateForReuse' '00236A60' ('00236AA6') | 'BattleUnit_ComputePresentationSuppressionMask' '003125E0' ('0031268A'): reason bit 1 of the mask that hides the actor (L-3, 2026-09-11) | | "

```
00234A80  mov      qword ptr [rsp + 8], rbx
00234A85  push     rdi
00234A86  sub      rsp, 0x20
00234A8A  xor      ebx, ebx
00234A8C  mov      edi, ecx
00234A8E  cmp      dword ptr [rip + 0x1e59c0c], ebx  ; -> 0208E6A0
00234A94  jle      0x234ad8  ; -> 00234AD8
00234A96  mov      ecx, ebx
00234A98  call     0x321170  ; -> 00321170 fn
00234A9D  test     rax, rax
00234AA0  je       0x234ace  ; -> 00234ACE
00234AA2  mov      rcx, qword ptr [rax + 0x698]
00234AA9  test     rcx, rcx
00234AAC  je       0x234ace  ; -> 00234ACE
00234AAE  cmp      byte ptr [rcx + 5], 1
00234AB2  jne      0x234ace  ; -> 00234ACE
00234AB4  movzx    ecx, byte ptr [rax + 0xe98]
00234ABB  bt       edi, ecx
00234ABE  jae      0x234ace  ; -> 00234ACE
00234AC0  and      dword ptr [rax], 0xfffff7ff
00234AC6  mov      rcx, rax
00234AC9  call     0x312700  ; -> 00312700 fn
00234ACE  inc      ebx
00234AD0  cmp      ebx, dword ptr [rip + 0x1e59bca]  ; -> 0208E6A0
00234AD6  jl       0x234a96  ; -> 00234A96
00234AD8  mov      rbx, qword ptr [rsp + 0x30]
00234ADD  add      rsp, 0x20
00234AE1  pop      rdi
00234AE2  ret      
```

## 0023B260 (49 B, extent 0023B260-0023B291)

Page context: "h 'edx' = '0xA' or '8' chosen by whether 'rbx' equals that record  Interior anchor '00469AE0' (function '00469A50').  '0026BBC0' (146 B) is the two-mode float-pair apply '002E8E20''s tail region and '0023B260'/'0026BB50'/'0026BD50' share: 'byte[rcx+3] >> 5' selects the lane - 1 writes the constant 1.0f pair into '[rcx+0xB8]+0x40' through '003DA860', 3 runs '003DA860' on '[+0xB8]+0x70'/'+0x90' with the live '+0x20'/'+0x28' floats and cle"

```
0023B260  push     rbx
0023B262  sub      rsp, 0x20
0023B266  movss    xmm1, dword ptr [rip + 0x6c68ce]  ; -> 00901B3C [f32 1.5]
0023B26E  mov      rbx, rcx
0023B271  movaps   xmm2, xmm1
0023B274  call     0x26bbc0  ; -> 0026BBC0 fn
0023B279  movss    xmm1, dword ptr [rip + 0x1ab09ef]  ; -> 01CEBC70 [f32 4]
0023B281  mov      rcx, rbx
0023B284  movaps   xmm2, xmm1
0023B287  add      rsp, 0x20
0023B28B  pop      rbx
0023B28C  jmp      0x26bf60  ; -> 0026BF60 fn
```

## 00263980 (4 B, extent 00263980-00263984)

Page context: "he '00234200' exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)  '00234200' = 'ActorSystem_ReleaseBattleUnitSlotForActor' (~215 B): '00263E30' unit resolve ('00234210'), member '00263980' word read ('00234220'), member tail '003589A0' ('00234232'); the release arm runs '00300140(rbx, 1)' / '00319140(rbx, 2)' ('0023423F'/'0023424C'), reads the stats record '[rbx+0x698]' ('byte[+5]' vs 1, 'dword[+0x64]', '0023425D'/'"

```
00263980  movzx    eax, word ptr [rcx]
00263983  ret      
```

## 002646A0 (32 B, extent 002646A0-002646C0)

Page context: "(eax <= 1)' — the availability boolean the unit paths read. Interior anchor '0030BCBB' (the compare).  '00313F80' (115 B) — reached through its '003357B0'/'003377C0'/ '00338490'/'0033C310' callers — '002646A0'-resolves both arguments, runs '00314F50(rsi, rax, 0, &out)' when both resolve, and publishes the result float to '*[r8]' when an out pointer is given; returns the both-resolved bool. Interior anchor '00313FBD' (the '00314F50' call"

```
002646A0  test     rcx, rcx
002646A3  je       0x2646bd  ; -> 002646BD
002646A5  mov      rax, qword ptr [rcx + 0xc0]
002646AC  test     rax, rax
002646AF  je       0x2646bd  ; -> 002646BD
002646B1  mov      rax, qword ptr [rax + 0x138]
002646B8  test     rax, rax
002646BB  jne      0x2646bf  ; -> 002646BF
002646BD  xor      eax, eax
002646BF  ret      
```

## 002659A0 (40 B, extent 002659A0-002659C8)

Page context: " + '0026B4A0([+0x10], 0xA)') and the '+0x58' category branch — mode 4 is rewritten to 1 here ('00238DBD'–'00238DC7', the spawn-record flag interaction the '+0x058' row already notes) and mode 1 runs '002659A0' + '0025D5E0([+0x10], 0xA)'.  | member | role | interior | | --- | --- | --- | | '00269F30' (9 B) | null-gated '+0xF' byte store on the '[+0x698]' child — the runtime sub-category write | ['00269F35'](../../_index/ADDRESS-INDEX.md)"

```
002659A0  movzx    eax, byte ptr [rcx + 3]
002659A4  and      dword ptr [rcx + 0x1c], 0xffffdeff
002659AB  and      al, 0xe0
002659AD  cmp      al, 0x60
002659AF  jne      0x2659b8  ; -> 002659B8
002659B1  and      dword ptr [rcx + 0x1c], 0xffffdeff
002659B8  and      byte ptr [rcx + 0xe], 0xf5
002659BC  or       byte ptr [rcx + 0xe], 5
002659C0  mov      byte ptr [rcx + 0xf4], 0
002659C7  ret      
```

## 00267CC0 (125 B, extent 00267CC0-00267D3D)

Page context: "ree '[+0xE60]' words '+0xA'/'+0xC'/'+0xE' against 'float[00843134]', unpacks '[+0xE68]+0x12' bits 4/6 and '[+0xE60]+3' bit 5 ('00238D6C'–'00238D94'), and chooses between the '[+0x6A0]'-bit-5 branch ('00267CC0' + '0026B4A0([+0x10], 0xA)') and the '+0x58' category branch — mode 4 is rewritten to 1 here ('00238DBD'–'00238DC7', the spawn-record flag interaction the '+0x058' row already notes) and mode 1 runs '002659A0' + '0025D5E0([+0x10], "

```
00267CC0  push     rbx
00267CC2  sub      rsp, 0x20
00267CC6  and      dword ptr [rcx + 0x1c], 0xfffffff7
00267CCA  mov      rbx, rcx
00267CCD  or       dword ptr [rcx + 0x1c], 0x100
00267CD4  test     byte ptr [rcx + 0xb], 8
00267CD8  je       0x267cdf  ; -> 00267CDF
00267CDA  call     0x268ea0  ; -> 00268EA0 fn
00267CDF  or       dword ptr [rbx + 0x1c], 0x2000
00267CE6  test     byte ptr [rbx + 0xb], 8
00267CEA  je       0x267cf4  ; -> 00267CF4
00267CEC  mov      rcx, rbx
00267CEF  call     0x268ea0  ; -> 00268EA0 fn
00267CF4  movzx    eax, byte ptr [rbx + 3]
00267CF8  and      al, 0xe0
00267CFA  cmp      al, 0x60
00267CFC  jne      0x267d28  ; -> 00267D28
00267CFE  or       dword ptr [rbx + 0x1c], 0x100
00267D05  test     byte ptr [rbx + 0xb], 8
00267D09  je       0x267d13  ; -> 00267D13
00267D0B  mov      rcx, rbx
00267D0E  call     0x268ea0  ; -> 00268EA0 fn
00267D13  or       dword ptr [rbx + 0x1c], 0x2000
00267D1A  test     byte ptr [rbx + 0xb], 8
00267D1E  je       0x267d28  ; -> 00267D28
00267D20  mov      rcx, rbx
00267D23  call     0x268ea0  ; -> 00268EA0 fn
00267D28  and      byte ptr [rbx + 0xe], 0xf4
00267D2C  or       byte ptr [rbx + 0xe], 4
00267D30  mov      byte ptr [rbx + 0xf4], 2
00267D37  add      rsp, 0x20
00267D3B  pop      rbx
00267D3C  ret      
```

## 0026BB50 (8 B, extent 0026BB50-0026BB58)

Page context: "0xA' or '8' chosen by whether 'rbx' equals that record  Interior anchor '00469AE0' (function '00469A50').  '0026BBC0' (146 B) is the two-mode float-pair apply '002E8E20''s tail region and '0023B260'/'0026BB50'/'0026BD50' share: 'byte[rcx+3] >> 5' selects the lane - 1 writes the constant 1.0f pair into '[rcx+0xB8]+0x40' through '003DA860', 3 runs '003DA860' on '[+0xB8]+0x70'/'+0x90' with the live '+0x20'/'+0x28' floats and clears 'byte[+"

```
0026BB50  movaps   xmm2, xmm1
0026BB53  jmp      0x26bbc0  ; -> 0026BBC0 fn
```

## 0026BD50 (113 B, extent 0026BD50-0026BDC1)

Page context: " chosen by whether 'rbx' equals that record  Interior anchor '00469AE0' (function '00469A50').  '0026BBC0' (146 B) is the two-mode float-pair apply '002E8E20''s tail region and '0023B260'/'0026BB50'/'0026BD50' share: 'byte[rcx+3] >> 5' selects the lane - 1 writes the constant 1.0f pair into '[rcx+0xB8]+0x40' through '003DA860', 3 runs '003DA860' on '[+0xB8]+0x70'/'+0x90' with the live '+0x20'/'+0x28' floats and clears 'byte[+0xDE]'; oth"

```
0026BD50  movzx    edx, byte ptr [rcx + 3]
0026BD54  xorps    xmm0, xmm0
0026BD57  cvtss2sd xmm0, xmm1
0026BD5B  shr      edx, 5
0026BD5E  andps    xmm0, xmmword ptr [rip + 0x1a8001b]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026BD65  cvtpd2ps xmm1, xmm0
0026BD69  xorps    xmm0, xmm0
0026BD6C  cvtss2sd xmm0, xmm2
0026BD70  andps    xmm0, xmmword ptr [rip + 0x1a80009]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026BD77  cvtpd2ps xmm4, xmm0
0026BD7B  sub      edx, 1
0026BD7E  je       0x26bd8d  ; -> 0026BD8D
0026BD80  cmp      edx, 2
0026BD83  jne      0x26bdc0  ; -> 0026BDC0
0026BD85  movaps   xmm2, xmm4
0026BD88  jmp      0x26bbc0  ; -> 0026BBC0 fn
0026BD8D  mov      rax, qword ptr [rcx + 0xb8]
0026BD94  or       byte ptr [rax + 0x5d], 4
0026BD98  movss    xmm2, dword ptr [rax + 0x30]
0026BD9D  comiss   xmm1, xmm2
0026BDA0  movss    xmm0, dword ptr [rax + 0x34]
0026BDA5  movss    dword ptr [rax + 0x40], xmm1
0026BDAA  movss    dword ptr [rax + 0x44], xmm4
0026BDAF  jbe      0x26bdb6  ; -> 0026BDB6
0026BDB1  movss    dword ptr [rax + 0x40], xmm2
0026BDB6  comiss   xmm4, xmm0
0026BDB9  jbe      0x26bdc0  ; -> 0026BDC0
0026BDBB  movss    dword ptr [rax + 0x44], xmm0
0026BDC0  ret      
```

## 0028A350 (499 B, extent 0028A350-0028A543)

Page context: "rs drive. Interior anchor '002E5FF0' (the '002E8E20' tail jmp).  ## SWE2-EC7-103 update (2026-09-20) - '002718E0' measured  '002718E0' (121 B) is the angle-accumulate publish '00289D70', '00289F50', '0028A350' and '0028A620' call: 'ecx == 0' returns 0; '003588B0()' null also returns; otherwise '00265470' resolves the record against 'rsi'/'rsi + 4'/'rsi + 8', '00263940' answers a float which is divided by '[008F311C]' ('3.1415..') and ac"

```
0028A350  mov      r11, rsp
0028A353  push     rbx
0028A354  push     rsi
0028A355  sub      rsp, 0x78
0028A359  mov      rax, qword ptr [rip + 0x1cba4d0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0028A360  xor      rax, rsp
0028A363  mov      qword ptr [rsp + 0x50], rax
0028A368  mov      rbx, qword ptr [rcx + 0x428]
0028A36F  mov      rsi, rcx
0028A372  test     rbx, rbx
0028A375  je       0x28a52f  ; -> 0028A52F
0028A37B  mov      qword ptr [r11 + 0x10], rbp
0028A37F  mov      ebp, 0x100
0028A384  mov      qword ptr [r11 + 0x18], rdi
0028A388  mov      qword ptr [r11 + 0x20], r14
0028A38C  xor      r14d, r14d
0028A38F  mov      qword ptr [r11 - 0x18], r15
0028A393  mov      r15d, 0xfffe
0028A399  movaps   xmmword ptr [rsp + 0x60], xmm6
0028A39E  movss    xmm6, dword ptr [rip + 0x1a617ca]  ; -> 01CEBB70 [f32 0.5]
0028A3A6  nop      word ptr [rax + rax]
0028A3B0  mov      rdi, qword ptr [rbx + 0x18]
0028A3B4  xor      edx, edx
0028A3B6  mov      eax, 0x10
0028A3BB  div      dword ptr [rip + 0x1b73cf3]  ; -> 01DFE0B4 [u32 0x00000001]
0028A3C1  add      word ptr [rbx + 0x10], ax
0028A3C5  cmp      word ptr [rbx + 0x10], bp
0028A3C9  jl       0x28a3ee  ; -> 0028A3EE
0028A3CB  inc      word ptr [rbx + 0x12]
0028A3CF  movsx    eax, word ptr [rbx + 0x12]
0028A3D3  mov      word ptr [rbx + 0x10], bp
0028A3D7  mov      edx, dword ptr [rip + 0x1b73cd7]  ; -> 01DFE0B4 [u32 0x00000001]
0028A3DD  imul     ecx, edx, 0x3c
0028A3E0  cmp      eax, ecx
0028A3E2  jb       0x28a3ee  ; -> 0028A3EE
0028A3E4  movsx    eax, dx
0028A3E7  imul     ecx, eax, 0x3c
0028A3EA  mov      word ptr [rbx + 0x12], cx
0028A3EE  mov      ecx, dword ptr [rbx + 0xc]
0028A3F1  test     ecx, ecx
0028A3F3  je       0x28a49c  ; -> 0028A49C
0028A3F9  lea      rdx, [rsp + 0x40]
0028A3FE  call     0x2718e0  ; -> 002718E0 fn
0028A403  test     eax, eax
0028A405  jne      0x28a435  ; -> 0028A435
0028A407  movsx    eax, word ptr [rbx + 0x12]
0028A40B  mov      dword ptr [rbx + 0xc], r14d
0028A40F  mov      r8d, dword ptr [rip + 0x1b73c9e]  ; -> 01DFE0B4 [u32 0x00000001]
0028A416  imul     ecx, r8d, 0x3c
0028A41A  mov      edx, ecx
0028A41C  shr      edx, 2
0028A41F  sub      ecx, edx
0028A421  cmp      eax, ecx
0028A423  jae      0x28a49c  ; -> 0028A49C
0028A425  movsx    eax, r8w
0028A429  imul     ecx, eax, 0x3c
0028A42C  sub      cx, dx
0028A42F  mov      word ptr [rbx + 0x12], cx
0028A433  jmp      0x28a49c  ; -> 0028A49C
0028A435  movss    xmm0, dword ptr [rbx]
0028A439  lea      r8, [rsp + 0x40]
0028A43E  movss    dword ptr [rsp + 0x20], xmm0
0028A444  lea      rdx, [rsp + 0x20]
0028A449  movss    xmm1, dword ptr [rbx + 4]
0028A44E  lea      rcx, [rsp + 0x30]
0028A453  movss    dword ptr [rsp + 0x24], xmm1
0028A459  movaps   xmm3, xmm6
0028A45C  movss    xmm0, dword ptr [rbx + 8]
0028A461  movss    dword ptr [rsp + 0x28], xmm0
0028A467  mov      dword ptr [rsp + 0x4c], 0x3f800000
0028A46F  mov      dword ptr [rsp + 0x2c], 0x3f800000
0028A477  call     0x275490  ; -> 00275490 fn
0028A47C  movss    xmm0, dword ptr [rsp + 0x30]
0028A482  movss    dword ptr [rbx], xmm0
0028A486  movss    xmm1, dword ptr [rsp + 0x34]
0028A48C  movss    dword ptr [rbx + 4], xmm1
0028A491  movss    xmm0, dword ptr [rsp + 0x38]
0028A497  movss    dword ptr [rbx + 8], xmm0
0028A49C  mov      ecx, dword ptr [rbx + 0xc]
0028A49F  test     ecx, ecx
0028A4A1  je       0x28a4c2  ; -> 0028A4C2
0028A4A3  call     0x3588b0  ; -> 003588B0 fn
0028A4A8  test     rax, rax
0028A4AB  je       0x28a4c2  ; -> 0028A4C2
0028A4AD  cmp      word ptr [rbx + 0x10], bp
0028A4B1  jl       0x28a501  ; -> 0028A501
0028A4B3  imul     eax, dword ptr [rip + 0x1b73bfa], 0x3c  ; -> 01DFE0B4 [u32 0x00000001]
0028A4BA  movsx    ecx, word ptr [rbx + 0x12]
0028A4BE  cmp      ecx, eax
0028A4C0  jb       0x28a501  ; -> 0028A501
0028A4C2  cmp      qword ptr [rsi + 0x428], rbx
0028A4C9  jne      0x28a4d2  ; -> 0028A4D2
0028A4CB  mov      qword ptr [rsi + 0x428], rdi
0028A4D2  mov      rcx, qword ptr [rbx + 0x20]
0028A4D6  test     rcx, rcx
0028A4D9  je       0x28a4e3  ; -> 0028A4E3
0028A4DB  mov      rax, qword ptr [rbx + 0x18]
0028A4DF  mov      qword ptr [rcx + 0x18], rax
0028A4E3  mov      rcx, qword ptr [rbx + 0x18]
0028A4E7  test     rcx, rcx
0028A4EA  je       0x28a4f4  ; -> 0028A4F4
0028A4EC  mov      rax, qword ptr [rbx + 0x20]
0028A4F0  mov      qword ptr [rcx + 0x20], rax
0028A4F4  and      word ptr [rbx + 0x16], r15w
0028A4F9  mov      qword ptr [rbx + 0x18], r14
0028A4FD  mov      qword ptr [rbx + 0x20], r14
0028A501  mov      rbx, rdi
0028A504  test     rdi, rdi
0028A507  jne      0x28a3b0  ; -> 0028A3B0
0028A50D  movaps   xmm6, xmmword ptr [rsp + 0x60]
0028A512  mov      r15, qword ptr [rsp + 0x70]
0028A517  mov      r14, qword ptr [rsp + 0xa8]
0028A51F  mov      rdi, qword ptr [rsp + 0xa0]
0028A527  mov      rbp, qword ptr [rsp + 0x98]
0028A52F  mov      rcx, qword ptr [rsp + 0x50]
0028A534  xor      rcx, rsp
0028A537  call     0x808c40  ; -> 00808C40 fn
0028A53C  add      rsp, 0x78
0028A540  pop      rsi
0028A541  pop      rbx
0028A542  ret      
```

## 0028A620 (361 B, extent 0028A620-0028A789)

Page context: "ior anchor '002E5FF0' (the '002E8E20' tail jmp).  ## SWE2-EC7-103 update (2026-09-20) - '002718E0' measured  '002718E0' (121 B) is the angle-accumulate publish '00289D70', '00289F50', '0028A350' and '0028A620' call: 'ecx == 0' returns 0; '003588B0()' null also returns; otherwise '00265470' resolves the record against 'rsi'/'rsi + 4'/'rsi + 8', '00263940' answers a float which is divided by '[008F311C]' ('3.1415..') and accumulated into "

```
0028A620  mov      r11, rsp
0028A623  push     rbx
0028A624  push     rsi
0028A625  sub      rsp, 0x78
0028A629  mov      rax, qword ptr [rip + 0x1cba200]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0028A630  xor      rax, rsp
0028A633  mov      qword ptr [rsp + 0x50], rax
0028A638  mov      rbx, qword ptr [rcx + 0x430]
0028A63F  mov      rsi, rcx
0028A642  test     rbx, rbx
0028A645  je       0x28a775  ; -> 0028A775
0028A64B  mov      qword ptr [r11 + 0x10], rbp
0028A64F  xor      ebp, ebp
0028A651  mov      qword ptr [r11 + 0x18], rdi
0028A655  mov      qword ptr [r11 - 0x18], r14
0028A659  mov      r14d, 0x100
0028A65F  movaps   xmmword ptr [rsp + 0x60], xmm6
0028A664  movss    xmm6, dword ptr [rip + 0x1a61504]  ; -> 01CEBB70 [f32 0.5]
0028A66C  nop      dword ptr [rax]
0028A670  mov      ecx, dword ptr [rbx + 0xc]
0028A673  mov      rdi, qword ptr [rbx + 0x18]
0028A677  test     ecx, ecx
0028A679  je       0x28a6f5  ; -> 0028A6F5
0028A67B  lea      rdx, [rsp + 0x40]
0028A680  call     0x2718e0  ; -> 002718E0 fn
0028A685  test     eax, eax
0028A687  jne      0x28a68e  ; -> 0028A68E
0028A689  mov      dword ptr [rbx + 0xc], ebp
0028A68C  jmp      0x28a6f5  ; -> 0028A6F5
0028A68E  movss    xmm0, dword ptr [rbx]
0028A692  lea      r8, [rsp + 0x40]
0028A697  movss    dword ptr [rsp + 0x20], xmm0
0028A69D  lea      rdx, [rsp + 0x20]
0028A6A2  movss    xmm1, dword ptr [rbx + 4]
0028A6A7  lea      rcx, [rsp + 0x30]
0028A6AC  movss    dword ptr [rsp + 0x24], xmm1
0028A6B2  movaps   xmm3, xmm6
0028A6B5  movss    xmm0, dword ptr [rbx + 8]
0028A6BA  movss    dword ptr [rsp + 0x28], xmm0
0028A6C0  mov      dword ptr [rsp + 0x4c], 0x3f800000
0028A6C8  mov      dword ptr [rsp + 0x2c], 0x3f800000
0028A6D0  call     0x275490  ; -> 00275490 fn
0028A6D5  movss    xmm0, dword ptr [rsp + 0x30]
0028A6DB  movss    dword ptr [rbx], xmm0
0028A6DF  movss    xmm1, dword ptr [rsp + 0x34]
0028A6E5  movss    dword ptr [rbx + 4], xmm1
0028A6EA  movss    xmm0, dword ptr [rsp + 0x38]
0028A6F0  movss    dword ptr [rbx + 8], xmm0
0028A6F5  xor      edx, edx
0028A6F7  mov      eax, 6
0028A6FC  div      dword ptr [rip + 0x1b739b2]  ; -> 01DFE0B4 [u32 0x00000001]
0028A702  add      word ptr [rbx + 0x10], ax
0028A706  cmp      word ptr [rbx + 0x10], r14w
0028A70B  jl       0x28a74f  ; -> 0028A74F
0028A70D  mov      word ptr [rbx + 0x12], bp
0028A711  cmp      rbx, qword ptr [rsi + 0x430]
0028A718  jne      0x28a721  ; -> 0028A721
0028A71A  mov      qword ptr [rsi + 0x430], rdi
0028A721  mov      rcx, qword ptr [rbx + 0x18]
0028A725  test     rcx, rcx
0028A728  je       0x28a732  ; -> 0028A732
0028A72A  mov      rax, qword ptr [rbx + 0x20]
0028A72E  mov      qword ptr [rcx + 0x20], rax
0028A732  mov      rcx, qword ptr [rbx + 0x20]
0028A736  test     rcx, rcx
0028A739  je       0x28a743  ; -> 0028A743
0028A73B  mov      rax, qword ptr [rbx + 0x18]
0028A73F  mov      qword ptr [rcx + 0x18], rax
0028A743  mov      qword ptr [rbx + 0x18], rbp
0028A747  mov      qword ptr [rbx + 0x20], rbp
0028A74B  mov      word ptr [rbx + 0x12], bp
0028A74F  mov      rbx, rdi
0028A752  test     rdi, rdi
0028A755  jne      0x28a670  ; -> 0028A670
0028A75B  movaps   xmm6, xmmword ptr [rsp + 0x60]
0028A760  mov      r14, qword ptr [rsp + 0x70]
0028A765  mov      rdi, qword ptr [rsp + 0xa0]
0028A76D  mov      rbp, qword ptr [rsp + 0x98]
0028A775  mov      rcx, qword ptr [rsp + 0x50]
0028A77A  xor      rcx, rsp
0028A77D  call     0x808c40  ; -> 00808C40 fn
0028A782  add      rsp, 0x78
0028A786  pop      rsi
0028A787  pop      rbx
0028A788  ret      
```

## 002E86B0 (69 B, extent 002E86B0-002E86F5)

Page context: "on's '+0x13 ≠ 0xFF' ('00239E3D'–'00239E5C'); a model without section 9 (every weapon) yields the engine's default table. '+0x184' is forwarded to the render record's '+0x420' ('0023A006'–'0023A012', '002E86B0'). In the party files opened slots 0–2 are '0.0667 / 0.1333 / 0.2' and slots 3, 4, 38, 39, 47 are angles ('0.1047' = 6°, '0.7854' = 45°); the monster's alternate slots 6–8 are '0.1333 / 0.2667 / 0.4'. One consumer is now known: '+0"

```
002E86B0  test     rcx, rcx
002E86B3  je       0x2e86f4  ; -> 002E86F4
002E86B5  mov      rax, qword ptr [rcx + 0xc0]
002E86BC  test     rax, rax
002E86BF  je       0x2e86f4  ; -> 002E86F4
002E86C1  cmp      dword ptr [rax], -1
002E86C4  je       0x2e86f4  ; -> 002E86F4
002E86C6  movzx    ecx, word ptr [rax]
002E86C9  cmp      cx, -1
002E86CD  je       0x2e86f4  ; -> 002E86F4
002E86CF  movsx    rax, cx
002E86D3  imul     rcx, rax, 0x740
002E86DA  add      rcx, qword ptr [rip + 0x1fde847]  ; -> 022C6F28
002E86E1  je       0x2e86f4  ; -> 002E86F4
002E86E3  cmp      dword ptr [rcx + 0x284], 0
002E86EA  je       0x2e86f4  ; -> 002E86F4
002E86EC  movss    dword ptr [rcx + 0x420], xmm1
002E86F4  ret      
```

## 002E9780 (36 B, extent 002E9780-002E97A4)

Page context: "ation — frontier hub 0026A330 (2026-09-18, SWE2-EC7)  **0026A330** ('Actor_SetMovementSpeed', 37 B, 4 A-measured callers) — the setter the field map's movement-speed entry reaches. 'Actor_IsLocked' ('002E9780') vetoes; then 'jae'-clamps a float parameter and tails '0026D6F0' — the same request channel 'Actor_StopRequestedMovement' ends on. So '+0x44'-block writes come in two forms: bulk zero (stop) or a single scaled value (this), both "

```
002E9780  movzx    eax, byte ptr [rcx + 3]
002E9784  and      al, 0xe0
002E9786  cmp      al, 0x60
002E9788  jne      0x2e97a1  ; -> 002E97A1
002E978A  mov      rax, qword ptr [rcx + 0xc0]
002E9791  test     rax, rax
002E9794  je       0x2e97a1  ; -> 002E97A1
002E9796  movzx    eax, byte ptr [rax + 0x11]
002E979A  shr      eax, 6
002E979D  and      eax, 1
002E97A0  ret      
002E97A1  xor      eax, eax
002E97A3  ret      
```

## 00346C00 (269 B, extent 00346C00-00346D0D)

Page context: "tion 'or' / 'and' / 'bts' / 'btr' forms; '00227680' also sets bit 24 with bit 27 through a register ('00227BC8', '00227BD7'), and byte-width writers at '+3' in '003DE710', '003EDAD0', '00517650' and '00346C00' are on unidentified objects.)* | | 25 | '0x2000000' | '00313500' ('00313531') | '003083A0' ('003083A0') |  | | 26 | '0x4000000' | 'Spawn_SelectPreviousMapEntry' '002354F0' ('0023557E'); '00238FA0' ('00238FAE'); 'SpawnEntry_SetCurr"

```
00346C00  mov      qword ptr [rsp + 0x18], rbx
00346C05  mov      qword ptr [rsp + 0x20], rbp
00346C0A  push     rsi
00346C0B  push     rdi
00346C0C  push     r14
00346C0E  sub      rsp, 0x20
00346C12  or       byte ptr [r8 + 3], 0x40
00346C17  mov      r14, rcx
00346C1A  movzx    ecx, byte ptr [rdx + 0x15]
00346C1E  mov      rdi, r9
00346C21  mov      rbx, r8
00346C24  mov      rbp, rdx
00346C27  call     0x267310  ; -> 00267310 fn
00346C2C  mov      rcx, rdi
00346C2F  test     eax, eax
00346C31  je       0x346cb7  ; -> 00346CB7
00346C37  mov      qword ptr [rsp + 0x40], r12
00346C3C  mov      qword ptr [rsp + 0x48], r15
00346C41  call     0x267e10  ; -> 00267E10 fn
00346C46  mov      rcx, rdi
00346C49  mov      r15d, eax
00346C4C  call     0x267e10  ; -> 00267E10 fn
00346C51  mov      rcx, rdi
00346C54  mov      r12d, eax
00346C57  call     0x267e10  ; -> 00267E10 fn
00346C5C  mov      esi, eax
00346C5E  test     eax, eax
00346C60  jns      0x346c69  ; -> 00346C69
00346C62  call     0x2dec00  ; -> 002DEC00 fn
00346C67  mov      esi, eax
00346C69  or       edx, 0xffffffff
00346C6C  mov      rcx, rdi
00346C6F  call     0x267f90  ; -> 00267F90 fn
00346C74  mov      edx, r12d
00346C77  mov      rcx, rdi
00346C7A  call     0x267f90  ; -> 00267F90 fn
00346C7F  mov      edx, r15d
00346C82  mov      rcx, rdi
00346C85  call     0x267f90  ; -> 00267F90 fn
00346C8A  mov      r9, rdi
00346C8D  mov      r8, rbx
00346C90  mov      rdx, rbp
00346C93  mov      rcx, r14
00346C96  call     0x345b60  ; -> 00345B60 fn
00346C9B  and      byte ptr [rbx + 3], 0x7f
00346C9F  xor      r8d, r8d
00346CA2  xor      edx, edx
00346CA4  mov      ecx, esi
00346CA6  call     0x360960  ; -> 00360960 fn
00346CAB  mov      r15, qword ptr [rsp + 0x48]
00346CB0  mov      r12, qword ptr [rsp + 0x40]
00346CB5  jmp      0x346cf6  ; -> 00346CF6
00346CB7  call     0x267e10  ; -> 00267E10 fn
00346CBC  mov      rcx, rdi
00346CBF  mov      esi, eax
00346CC1  call     0x267e10  ; -> 00267E10 fn
00346CC6  mov      rcx, rdi
00346CC9  mov      ebp, eax
00346CCB  call     0x267e10  ; -> 00267E10 fn
00346CD0  test     eax, eax
00346CD2  jns      0x346cd9  ; -> 00346CD9
00346CD4  call     0x2dec00  ; -> 002DEC00 fn
00346CD9  and      byte ptr [rbx + 2], 0xf
00346CDD  test     esi, esi
00346CDF  mov      dword ptr [rbx + 8], ebp
00346CE2  mov      word ptr [rbx], ax
00346CE5  setne    cl
00346CE8  and      byte ptr [rbx + 3], 0xc0
00346CEC  shl      cl, 4
00346CEF  or       byte ptr [rbx + 2], cl
00346CF2  or       byte ptr [rbx + 3], 0x80
00346CF6  mov      rbx, qword ptr [rsp + 0x50]
00346CFB  mov      rbp, qword ptr [rsp + 0x58]
00346D00  add      rsp, 0x20
00346D04  pop      r14
00346D06  pop      rdi
00346D07  pop      rsi
00346D08  jmp      0x25d5d0  ; -> 0025D5D0 fn
```

## 003589A0 (8 B, extent 003589A0-003589A8)

Page context: " bound (SWE2-FRONTIER, followup queue)  '00234200' = 'ActorSystem_ReleaseBattleUnitSlotForActor' (~215 B): '00263E30' unit resolve ('00234210'), member '00263980' word read ('00234220'), member tail '003589A0' ('00234232'); the release arm runs '00300140(rbx, 1)' / '00319140(rbx, 2)' ('0023423F'/'0023424C'), reads the stats record '[rbx+0x698]' ('byte[+5]' vs 1, 'dword[+0x64]', '0023425D'/'00234268'), '00313F60' ('00234275'), copies 'dw"

```
003589A0  movzx    eax, byte ptr [rcx + 3]
003589A4  shr      eax, 5
003589A7  ret      
```

## 00468D10 (53 B, extent 00468D10-00468D45)

Page context: "or '00391EBE' (an '003912E0' call).  ## SWE2-EC7-35 update (2026-09-19) - '00391A30'  '00391A30' (721 B) is a battle-unit field body - '02AEE0A0'/'02AEE0B8'/'02AEE0B0'/'02AEE090' records, '00469060'/'00468D10'/'002FB500'/'002FB340'/'00861EC0'. Interior anchor '00391AAB' (an '00861EC0' call).  ## SWE2-EC7-37 update (2026-09-19) - '003377C0'  '003377C0' (565 B) is a battle-unit field path - '01F44830', '0031ABE0' flag-gate consult plus '0"

```
00468D10  movss    xmm2, dword ptr [rcx]
00468D14  xor      eax, eax
00468D16  movss    xmm1, dword ptr [rcx + 8]
00468D1B  subss    xmm1, dword ptr [rdx + 8]
00468D20  subss    xmm2, dword ptr [rdx]
00468D24  movss    xmm0, dword ptr [rcx + 0x10]
00468D29  addss    xmm0, dword ptr [rdx + 0x10]
00468D2E  mulss    xmm1, xmm1
00468D32  mulss    xmm2, xmm2
00468D36  mulss    xmm0, xmm0
00468D3A  addss    xmm1, xmm2
00468D3E  comiss   xmm0, xmm1
00468D41  seta     al
00468D44  ret      
```

## 00468F70 (17 B, extent 00468F70-00468F81)

Page context: "ment layer — '00202B10' alone is called by '00334220'/'003347C0'/'00334E00'/'00335B60' — and the '00469410' per-axis interpolator this page measured is itself called by the Movement-owned '00468A70'/'00468F70'. Consultation in both directions, no shared ownership.  **Presentation — CLIENT (SWE2-EC7-167, 200 edges).** '003B0980' — the '02EBEC18' first-zero-field locator this page measured — is called by '003B02A0', owned by that layer, a"

```
00468F70  movss    xmm2, dword ptr [rcx + 0x20]
00468F75  mov      r9, rdx
00468F78  lea      rdx, [rcx + 0x10]
00468F7C  jmp      0x469410  ; -> 00469410 fn
```

## 00469060 (79 B, extent 00469060-004690AF)

Page context: "terior anchor '00391EBE' (an '003912E0' call).  ## SWE2-EC7-35 update (2026-09-19) - '00391A30'  '00391A30' (721 B) is a battle-unit field body - '02AEE0A0'/'02AEE0B8'/'02AEE0B0'/'02AEE090' records, '00469060'/'00468D10'/'002FB500'/'002FB340'/'00861EC0'. Interior anchor '00391AAB' (an '00861EC0' call).  ## SWE2-EC7-37 update (2026-09-19) - '003377C0'  '003377C0' (565 B) is a battle-unit field path - '01F44830', '0031ABE0' flag-gate cons"

```
00469060  mov      qword ptr [rsp + 8], rbx
00469065  push     rdi
00469066  sub      rsp, 0x20
0046906A  mov      rbx, rdx
0046906D  mov      rdi, rcx
00469070  call     0x468580  ; -> 00468580 fn
00469075  movss    xmm2, dword ptr [rbx]
00469079  xor      eax, eax
0046907B  movss    xmm1, dword ptr [rbx + 8]
00469080  subss    xmm1, dword ptr [rdi + 8]
00469085  addss    xmm0, dword ptr [rbx + 0x10]
0046908A  subss    xmm2, dword ptr [rdi]
0046908E  mov      rbx, qword ptr [rsp + 0x30]
00469093  mulss    xmm1, xmm1
00469097  mulss    xmm2, xmm2
0046909B  mulss    xmm0, xmm0
0046909F  addss    xmm1, xmm2
004690A3  comiss   xmm0, xmm1
004690A6  setae    al
004690A9  add      rsp, 0x20
004690AD  pop      rdi
004690AE  ret      
```
