# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/effect-element-type-dispatch.json`.

Functions: 56. Each is cited on the page only at its entry and is still in the F frontier.

## 001DB340 (134 B, extent 001DB340-001DB3C6)

Page context: "0540E47  call 001DB7E0                    ; a 0x640 GiVmax command, stored at node+8 00540E4C  shl  r12d, 4                     ; the table's byte length    per descriptor, by its tag nibble:      1  001DB340(cmd, desc + 8, len*0x10 + 8)        ; appended IN PLACE, advance 8 + that      3  0019C5A0(len*0x10 + 8); copy qword[desc+8]; memcpy the payload behind it;         001DB340(cmd, copy, len*0x10 + 8)            ; advance 0x10 00540F3"

```
001DB340  mov      qword ptr [rsp + 8], rbx
001DB345  push     rdi
001DB346  sub      rsp, 0x30
001DB34A  mov      eax, dword ptr [rcx + 0x1c]
001DB34D  lea      rbx, [rcx + 0x18]
001DB351  mov      qword ptr [rsp + 0x20], rdx
001DB356  xor      edx, edx
001DB358  div      dword ptr [rbx]
001DB35A  mov      dword ptr [rsp + 0x28], r8d
001DB35F  cmp      eax, 0x40
001DB362  jb       0x1db36f  ; -> 001DB36F
001DB364  mov      dword ptr [0], 0
001DB36F  cmp      qword ptr [rbx + rax*8 + 8], 0
001DB375  lea      rdi, [rbx + rax*8]
001DB379  jne      0x1db39f  ; -> 001DB39F
001DB37B  mov      edx, dword ptr [rbx]
001DB37D  mov      rcx, qword ptr [rip + 0x1da413c]  ; -> 01F7F4C0
001DB384  shl      edx, 4
001DB387  call     0x1a1470  ; -> 001A1470 fn
001DB38C  mov      qword ptr [rdi + 8], rax
001DB390  mov      rdx, rax
001DB393  mov      rcx, qword ptr [rip + 0x1da4126]  ; -> 01F7F4C0
001DB39A  call     0x16d6a0  ; -> 0016D6A0 fn
001DB39F  mov      eax, dword ptr [rbx + 4]
001DB3A2  xor      edx, edx
001DB3A4  div      dword ptr [rbx]
001DB3A6  mov      rax, qword ptr [rdi + 8]
001DB3AA  movups   xmm0, xmmword ptr [rsp + 0x20]
001DB3AF  mov      ecx, edx
001DB3B1  add      rcx, rcx
001DB3B4  movups   xmmword ptr [rax + rcx*8], xmm0
001DB3B8  inc      dword ptr [rbx + 4]
001DB3BB  mov      rbx, qword ptr [rsp + 0x40]
001DB3C0  add      rsp, 0x30
001DB3C4  pop      rdi
001DB3C5  ret      
```

## 0020E610 (8 B, extent 0020E610-0020E618)

Page context: "bx+0x20]', 'byte[rsi+0x2A7]' bits 1/2/4 each run '003A6E60(2)' whose 'al & 1' merges into 'byte[rbx+0x2A4]' bits 0/1/2 ('& 0xFE'/'& 0xFD'/'& 0xFB' clears first), and '00459BD0'/'0044B960'/'003D8E50'/'0020E610' commit - the '+0x2A7'-sourced sibling of '0045A050'/'00455390'.  Interior anchor '00459429' (function '00459420').  '00459BD0' (1086 B) is the third evaluator twin '00459420' commits to (also '004593E0'): identical '00430B90' comp"

```
0020E610  xor      eax, eax
0020E612  test     ecx, ecx
0020E614  sete     al
0020E617  ret      
```

## 00231820 (105 B, extent 00231820-00231889)

Page context: "'003590D0' callers are shared-accessor fan-in.  **Movement — SERVICE (SWE2-CONTRACT 2026-09-15, 18 edges).** '003A4290'/'003A56F0' call Movement helpers '0026E350' and '00264670' (which itself calls '00231820'/'00231900') while positioning elements. The fourteen caller edges are Movement bodies sharing '003590D0' ('Movement_UpdateSteeringTowardTarget', 'PartyFollow_SolveFormation', 'BattleUnit_CanAdvanceCombatNavigation', 'Movement_SetR"

```
00231820  movss    xmm0, dword ptr [rdx + 4]
00231825  test     r8w, r8w
00231829  js       0x231883  ; -> 00231883
0023182B  movsx    rax, r8w
0023182F  shl      rax, 5
00231833  add      rax, qword ptr [rcx + 0x10]
00231837  movsx    r8, word ptr [rax + 0x10]
0023183C  movss    xmm2, dword ptr [rax + 4]
00231841  shl      r8, 4
00231845  add      r8, qword ptr [rcx + 8]
00231849  comiss   xmm2, dword ptr [rip + 0x6942dc]  ; -> 008C5B2C [f32 0.001]
00231850  jbe      0x231883  ; -> 00231883
00231852  movss    xmm1, dword ptr [r8 + 8]
00231858  subss    xmm1, dword ptr [rdx + 8]
0023185D  movss    xmm0, dword ptr [r8]
00231862  subss    xmm0, dword ptr [rdx]
00231866  mulss    xmm1, dword ptr [rax + 8]
0023186B  mulss    xmm0, dword ptr [rax]
0023186F  addss    xmm1, xmm0
00231873  divss    xmm1, xmm2
00231877  addss    xmm1, dword ptr [r8 + 4]
0023187D  movss    dword ptr [rdx + 4], xmm1
00231882  ret      
00231883  movss    dword ptr [rdx + 4], xmm0
00231888  ret      
```

## 0024B1C0 (43 B, extent 0024B1C0-0024B1EB)

Page context: "calls 'not read' | | '0x60'–'0x74' (main '0x60'–'0x67' + sub '0x68'–'0x74') | [the-element-types-60-74](the-element-types-60-74.md) | record maps + helper roles (PRNG '0044B960', deferred-free queue '0024B1C0'); '0x70' confirmed definition-only; tails 'not read' | | '0x80'–'0x97' | [the-element-types-80-97](the-element-types-80-97.md) | shared-method band: sibling types share step/update/setup; variant-selector walks found (record flag "

```
0024B1C0  movzx    eax, word ptr [rip + 0x1e46fa1]  ; -> 02092168
0024B1C7  mov      edx, 0x100
0024B1CC  cmp      ax, dx
0024B1CF  jae      0x3697f0  ; -> 003697F0 fn
0024B1D5  movzx    eax, ax
0024B1D8  lea      rdx, [rip + 0x1e45f71]  ; -> 02091150
0024B1DF  mov      qword ptr [rdx + rax*8], rcx
0024B1E3  inc      word ptr [rip + 0x1e46f7e]  ; -> 02092168
0024B1EA  ret      
```

## 002F3890 (122 B, extent 002F3890-002F390A)

Page context: "elocity '+0xB4' (sign mask '[01CEBDA0]') and damps it by byte '+0x46' percent ('[008F3134]' = 100) ('002F2A00'..'002F2A4E'), a bounce; 2 makes the same test and, when above, ends the element through '002F3890', '003A8950(3, element)' and '002F31C0' ('002F2A50'..'002F2A5F', '002F2D37'..'002F2D52'). The three angle accumulators '+0xE0', '+0xE4', '+0xE8' are then wrapped by one turn, '[01CEBC78]' = 2π down and '[00915624]' = -2π up ('002F2"

```
002F3890  push     rbx
002F3892  sub      rsp, 0x40
002F3896  mov      rax, qword ptr [rip + 0x1c50f93]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002F389D  xor      rax, rsp
002F38A0  mov      qword ptr [rsp + 0x30], rax
002F38A5  mov      eax, dword ptr [rcx + 0x1f0]
002F38AB  mov      rbx, rcx
002F38AE  mov      dword ptr [rcx + 0x1f4], eax
002F38B4  mov      rcx, qword ptr [rcx + 0x10]
002F38B8  test     rcx, rcx
002F38BB  je       0x2f38e2  ; -> 002F38E2
002F38BD  movaps   xmm0, xmmword ptr [rbx + 0x60]
002F38C1  movdqa   xmmword ptr [rsp + 0x20], xmm0
002F38C7  call     0x39af70  ; -> 0039AF70 fn
002F38CC  lea      rdx, [rsp + 0x20]
002F38D1  lea      rcx, [rsp + 0x20]
002F38D6  call     0x398f90  ; -> 00398F90 fn
002F38DB  movaps   xmm1, xmmword ptr [rsp + 0x20]
002F38E0  jmp      0x2f38e6  ; -> 002F38E6
002F38E2  movaps   xmm1, xmmword ptr [rbx + 0x60]
002F38E6  movaps   xmm0, xmmword ptr [rbx + 0x70]
002F38EA  movdqa   xmmword ptr [rbx + 0x80], xmm0
002F38F2  movdqa   xmmword ptr [rbx + 0x70], xmm1
002F38F7  mov      rcx, qword ptr [rsp + 0x30]
002F38FC  xor      rcx, rsp
002F38FF  call     0x808c40  ; -> 00808C40 fn
002F3904  add      rsp, 0x40
002F3908  pop      rbx
002F3909  ret      
```

## 00333C00 (113 B, extent 00333C00-00333C71)

Page context: "plus '022D91E0'/'022D9230' tables. Interior anchor '0046F580' (a '0036DD80' call).  ## SWE2-EC7-54 update (2026-09-19) - '003A75B0'  '003A75B0' (312 B) is an effect-file data-parse body - '0020E600'/'00333C00'/'003697F0' plus '02EBEFA8'/'02F97340'. Interior anchor '003A7602' (a '0020E600' call).  ## SWE2-EC7-57 update (2026-09-19) - '00503F50'  '00503F50' (171 B) is an effect-element '0x57'-kind body - '0020E600'/'0020E620'/'003697F0'/'"

```
00333C00  mov      qword ptr [rsp + 8], rbx
00333C05  mov      qword ptr [rsp + 0x10], rsi
00333C0A  push     rdi
00333C0B  sub      rsp, 0x20
00333C0F  lea      rdi, [rcx + 0x2c]
00333C13  mov      esi, 0x1d
00333C18  mov      rbx, rdi
00333C1B  nop      dword ptr [rax + rax]
00333C20  mov      ecx, dword ptr [rbx]
00333C22  call     0x20e600  ; -> 0020E600 fn
00333C27  test     rax, rax
00333C2A  je       0x333c53  ; -> 00333C53
00333C2C  mov      ecx, dword ptr [rbx]
00333C2E  call     0x20e600  ; -> 0020E600 fn
00333C33  mov      rcx, rax
00333C36  call     0x46f370  ; -> 0046F370 fn
00333C3B  mov      ecx, dword ptr [rbx]
00333C3D  call     0x20e600  ; -> 0020E600 fn
00333C42  mov      rcx, rax
00333C45  call     0x3697f0  ; -> 003697F0 fn
00333C4A  xor      ecx, ecx
00333C4C  call     0x20e620  ; -> 0020E620 fn
00333C51  mov      dword ptr [rdi], eax
00333C53  add      rbx, 4
00333C57  add      rdi, 4
00333C5B  sub      rsi, 1
00333C5F  jne      0x333c20  ; -> 00333C20
00333C61  mov      rbx, qword ptr [rsp + 0x30]
00333C66  mov      rsi, qword ptr [rsp + 0x38]
00333C6B  add      rsp, 0x20
00333C6F  pop      rdi
00333C70  ret      
```

## 00350DD0 (238 B, extent 00350DD0-00350EBE)

Page context: ", 'offsetsoftimage', the battle-script 'btlAtelGetMyPosX'/'Y'/'Z' and 'debug_getucpcpos' read an actor's position through the getter an element's world anchor uses (representative: 'checkdistance3d' '00350DD0'). - *'InputDevice_QueryAvailabilityState_Always1' '0053DD10', 17 edges - MECHANICAL.* The body is 'mov eax, 1; ret'. The script's sync polls ('modelreadsync', 'musicreadsync', 'effectreadsync', 'voicereadsync', 'motionreadsync', '"

```
00350DD0  mov      qword ptr [rsp + 8], rbx
00350DD5  mov      qword ptr [rsp + 0x10], rbp
00350DDA  mov      qword ptr [rsp + 0x18], rsi
00350DDF  push     rdi
00350DE0  sub      rsp, 0x40
00350DE4  mov      rbp, rcx
00350DE7  movaps   xmmword ptr [rsp + 0x30], xmm6
00350DEC  mov      rcx, r9
00350DEF  mov      rbx, r9
00350DF2  xor      edi, edi
00350DF4  call     0x267db0  ; -> 00267DB0 fn
00350DF9  mov      rcx, rbx
00350DFC  movaps   xmm6, xmm0
00350DFF  call     0x267e10  ; -> 00267E10 fn
00350E04  mov      ebx, eax
00350E06  call     0x2640c0  ; -> 002640C0 fn
00350E0B  mov      edx, ebx
00350E0D  mov      rcx, rax
00350E10  call     0x358940  ; -> 00358940 fn
00350E15  mov      rsi, rax
00350E18  call     0x3590d0  ; -> 003590D0 fn
00350E1D  mov      ecx, eax
00350E1F  call     0x3588b0  ; -> 003588B0 fn
00350E24  test     rax, rax
00350E27  je       0x350e9b  ; -> 00350E9B
00350E29  test     rsi, rsi
00350E2C  je       0x350e9b  ; -> 00350E9B
00350E2E  mov      rbx, qword ptr [rax + 0xb8]
00350E35  lea      r9, [rsp + 0x28]
00350E3A  lea      r8, [rsp + 0x24]
00350E3F  mov      rcx, rsi
00350E42  lea      rdx, [rsp + 0x20]
00350E47  call     0x265020  ; -> 00265020 fn
00350E4C  movss    xmm2, dword ptr [rbx]
00350E50  mov      eax, 1
00350E55  subss    xmm2, dword ptr [rsp + 0x20]
00350E5B  mulss    xmm6, xmm6
00350E5F  movss    dword ptr [rsp + 0x20], xmm2
00350E65  movss    xmm0, dword ptr [rbx + 4]
00350E6A  subss    xmm0, dword ptr [rsp + 0x24]
00350E70  mulss    xmm2, xmm2
00350E74  movss    dword ptr [rsp + 0x24], xmm0
00350E7A  movss    xmm1, dword ptr [rbx + 8]
00350E7F  subss    xmm1, dword ptr [rsp + 0x28]
00350E85  mulss    xmm0, xmm0
00350E89  addss    xmm2, xmm0
00350E8D  mulss    xmm1, xmm1
00350E91  addss    xmm2, xmm1
00350E95  comiss   xmm6, xmm2
00350E98  cmova    edi, eax
00350E9B  mov      edx, edi
00350E9D  mov      rcx, rbp
00350EA0  mov      rbx, qword ptr [rsp + 0x50]
00350EA5  mov      rbp, qword ptr [rsp + 0x58]
00350EAA  mov      rsi, qword ptr [rsp + 0x60]
00350EAF  movaps   xmm6, xmmword ptr [rsp + 0x30]
00350EB4  add      rsp, 0x40
00350EB8  pop      rdi
00350EB9  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00377010 (119 B, extent 00377010-00377087)

Page context: "0').  '00461090' (441 B) is the flag compute '002F3BC0' calls: '002F2D60' gates, 'rdi = [rbx+0x20]', 'byte[rdi+0x1B4] & 4' gates, 'word[rdi+0x1CE] >> 5 & 1' feeds '00376350' into '[rbx+0x294]', then '00377010'/'003770D0'/'00377100'/'00399600'/'0039B550'/'0044B960'/'00462160'/'001827B0'/'00808C40' run the per-flag arms - the element's flag evaluator.  Interior anchor '004610B0' (function '00461090').  '00377100' (38 B) is the call-free s"

```
00377010  movzx    r8d, cl
00377014  lea      rax, [rip + 0x2764b25]  ; -> 02ADBB40
0037701B  lea      r9, [r8 + r8*8]
0037701F  shl      r9, 4
00377023  add      r9, rax
00377026  test     ecx, ecx
00377028  je       0x377086  ; -> 00377086
0037702A  cmp      dword ptr [r9], ecx
0037702D  jne      0x377086  ; -> 00377086
0037702F  movzx    eax, word ptr [r9 + 0x54]
00377034  xor      ax, word ptr [rdx]
00377037  and      ax, 1
0037703B  xor      word ptr [r9 + 0x54], ax
00377040  movzx    ecx, word ptr [rdx + 4]
00377044  add      cx, cx
00377047  xor      cx, word ptr [r9 + 0x54]
0037704C  and      cx, 2
00377050  xor      word ptr [r9 + 0x54], cx
00377055  mov      eax, dword ptr [rdx + 0x14]
00377058  mov      dword ptr [r9 + 0x40], eax
0037705C  mov      eax, dword ptr [rdx + 0x18]
0037705F  mov      dword ptr [r9 + 0x44], eax
00377063  mov      eax, dword ptr [rdx + 0x1c]
00377066  mov      dword ptr [r9 + 0x48], eax
0037706A  mov      eax, dword ptr [rdx + 0x20]
0037706D  mov      dword ptr [r9 + 0x4c], eax
00377071  mov      eax, dword ptr [rdx + 8]
00377074  mov      dword ptr [r9 + 0x34], eax
00377078  mov      eax, dword ptr [rdx + 0xc]
0037707B  mov      dword ptr [r9 + 0x38], eax
0037707F  mov      eax, dword ptr [rdx + 0x10]
00377082  mov      dword ptr [r9 + 0x3c], eax
00377086  ret      
```

## 0039D430 (68 B, extent 0039D430-0039D474)

Page context: "50' call).  ## SWE2-EC7-37 update (2026-09-19) - '003ED8A0'  '003ED8A0' (552 B) is the effect-file data parse - '02096D30'/'02096887'/'02096D34' (the effect camera), '003A9510'/'003A7CB0'/'003A75B0'/'0039D430'/'003CC0F0'/'003829D0'/'003A98D0'. Interior anchor '003ED909' (a '003A9510' call).  ## SWE2-EC7-37 update (2026-09-19) - '004352C0'  '004352C0' (537 B) is an element-record fill - '0020E600' 22-times/'003697F0' 11-times/'0020E620' "

```
0039D430  sub      rsp, 0x28
0039D434  movups   xmm0, xmmword ptr [rcx]
0039D437  movups   xmmword ptr [rip + 0x27515a2], xmm0  ; -> 02AEE9E0
0039D43E  movups   xmm1, xmmword ptr [rcx + 0x10]
0039D442  movups   xmmword ptr [rip + 0x27515a7], xmm1  ; -> 02AEE9F0
0039D449  movups   xmm0, xmmword ptr [rcx + 0x20]
0039D44D  movups   xmmword ptr [rip + 0x27515ac], xmm0  ; -> 02AEEA00
0039D454  movups   xmm1, xmmword ptr [rcx + 0x30]
0039D458  movups   xmmword ptr [rip + 0x27515b1], xmm1  ; -> 02AEEA10
0039D45F  call     0x39afa0  ; -> 0039AFA0 fn
0039D464  lea      rcx, [rip + 0x2751845]  ; -> 02AEECB0
0039D46B  add      rsp, 0x28
0039D46F  jmp      0x3970a0  ; -> 003970A0 fn
```

## 003A5640 (126 B, extent 003A5640-003A56BE)

Page context: "431770'. Interior anchor '00538EC9' (a '00500470' call).  ## SWE2-EC7-41 update (2026-09-19) - '003A6C30'  '003A6C30' (352 B) is an effect-element body - '01F44830'/'02096B24'/'022C6F28'/'02F97348', '003A5640'/'00421E20'/'00808C40'. Interior anchor '003A6CB8' (a '003A5640' call).  ## SWE2-EC7-43 update (2026-09-19) - '004427D0'  '004427D0' (277 B) is the '0x03' effect-element dispatch body - '01F44830'/'02AEE900'/'02AEE908', '0026EE00'/"

```
003A5640  sub      rsp, 0x28
003A5644  mov      r8, qword ptr [rip + 0x2bf1cfd]  ; -> 02F97348
003A564B  mov      eax, 0x200
003A5650  xor      edx, edx
003A5652  test     word ptr [r8 + 0x378], ax
003A565A  jne      0x3a5691  ; -> 003A5691
003A565C  cmp      byte ptr [r8], 3
003A5660  jne      0x3a5675  ; -> 003A5675
003A5662  cmp      ecx, -1
003A5665  cmovne   edx, ecx
003A5668  movsxd   rax, edx
003A566B  mov      eax, dword ptr [r8 + rax*4 + 0x10]
003A5670  add      rsp, 0x28
003A5674  ret      
003A5675  cmp      ecx, -1
003A5678  cmovne   edx, ecx
003A567B  movsxd   rax, edx
003A567E  mov      ecx, dword ptr [r8 + rax*4 + 0x90]
003A5686  test     ecx, ecx
003A5688  jne      0x3a56ac  ; -> 003A56AC
003A568A  mov      ecx, dword ptr [r8 + rax*4 + 0x10]
003A568F  jmp      0x3a56ac  ; -> 003A56AC
003A5691  cmp      ecx, -1
003A5694  cmovne   edx, ecx
003A5697  cmp      edx, dword ptr [rip + 0x1cf1487]  ; -> 02096B24
003A569D  jge      0x3a56b6  ; -> 003A56B6
003A569F  movsxd   rax, edx
003A56A2  lea      rcx, [rip + 0x1cf137b]  ; -> 02096A24
003A56A9  mov      ecx, dword ptr [rcx + rax*4]
003A56AC  call     0x2e9b80  ; -> 002E9B80 fn
003A56B1  cmp      eax, -1
003A56B4  jne      0x3a56b9  ; -> 003A56B9
003A56B6  or       eax, 0xffffffff
003A56B9  add      rsp, 0x28
003A56BD  ret      
```

## 003A7CB0 (78 B, extent 003A7CB0-003A7CFE)

Page context: "'00522AB9' (an '003D8E50' call).  ## SWE2-EC7-37 update (2026-09-19) - '003ED8A0'  '003ED8A0' (552 B) is the effect-file data parse - '02096D30'/'02096887'/'02096D34' (the effect camera), '003A9510'/'003A7CB0'/'003A75B0'/'0039D430'/'003CC0F0'/'003829D0'/'003A98D0'. Interior anchor '003ED909' (a '003A9510' call).  ## SWE2-EC7-37 update (2026-09-19) - '004352C0'  '004352C0' (537 B) is an element-record fill - '0020E600' 22-times/'003697F0"

```
003A7CB0  mov      qword ptr [rsp + 8], rbx
003A7CB5  push     rdi
003A7CB6  sub      rsp, 0x20
003A7CBA  xor      edi, edi
003A7CBC  mov      ebx, edi
003A7CBE  nop      
003A7CC0  mov      rax, qword ptr [rip + 0x2b172d9]  ; -> 02EBEFA0
003A7CC7  mov      rcx, qword ptr [rax]
003A7CCA  mov      rcx, qword ptr [rbx + rcx]
003A7CCE  test     rcx, rcx
003A7CD1  je       0x3a7ce6  ; -> 003A7CE6
003A7CD3  call     0x3697f0  ; -> 003697F0 fn
003A7CD8  mov      rax, qword ptr [rip + 0x2b172c1]  ; -> 02EBEFA0
003A7CDF  mov      rcx, qword ptr [rax]
003A7CE2  mov      qword ptr [rbx + rcx], rdi
003A7CE6  add      rbx, 8
003A7CEA  cmp      rbx, 0x400
003A7CF1  jl       0x3a7cc0  ; -> 003A7CC0
003A7CF3  mov      rbx, qword ptr [rsp + 0x30]
003A7CF8  add      rsp, 0x20
003A7CFC  pop      rdi
003A7CFD  ret      
```

## 003A9510 (79 B, extent 003A9510-003A955F)

Page context: "ior anchor '00522AB9' (an '003D8E50' call).  ## SWE2-EC7-37 update (2026-09-19) - '003ED8A0'  '003ED8A0' (552 B) is the effect-file data parse - '02096D30'/'02096887'/'02096D34' (the effect camera), '003A9510'/'003A7CB0'/'003A75B0'/'0039D430'/'003CC0F0'/'003829D0'/'003A98D0'. Interior anchor '003ED909' (a '003A9510' call).  ## SWE2-EC7-37 update (2026-09-19) - '004352C0'  '004352C0' (537 B) is an element-record fill - '0020E600' 22-time"

```
003A9510  mov      qword ptr [rsp + 8], rbx
003A9515  push     rdi
003A9516  sub      rsp, 0x20
003A951A  mov      ebx, 8
003A951F  xor      edi, edi
003A9521  mov      rax, qword ptr [rip + 0x2b15a68]  ; -> 02EBEF90
003A9528  mov      rcx, qword ptr [rax]
003A952B  mov      rcx, qword ptr [rbx + rcx]
003A952F  test     rcx, rcx
003A9532  je       0x3a9547  ; -> 003A9547
003A9534  call     0x3697f0  ; -> 003697F0 fn
003A9539  mov      rax, qword ptr [rip + 0x2b15a50]  ; -> 02EBEF90
003A9540  mov      rcx, qword ptr [rax]
003A9543  mov      qword ptr [rbx + rcx], rdi
003A9547  add      rbx, 8
003A954B  cmp      rbx, 0xa00
003A9552  jl       0x3a9521  ; -> 003A9521
003A9554  mov      rbx, qword ptr [rsp + 0x30]
003A9559  add      rsp, 0x20
003A955D  pop      rdi
003A955E  ret      
```

## 003A98D0 (79 B, extent 003A98D0-003A991F)

Page context: " (2026-09-19) - '003ED8A0'  '003ED8A0' (552 B) is the effect-file data parse - '02096D30'/'02096887'/'02096D34' (the effect camera), '003A9510'/'003A7CB0'/'003A75B0'/'0039D430'/'003CC0F0'/'003829D0'/'003A98D0'. Interior anchor '003ED909' (a '003A9510' call).  ## SWE2-EC7-37 update (2026-09-19) - '004352C0'  '004352C0' (537 B) is an element-record fill - '0020E600' 22-times/'003697F0' 11-times/'0020E620' 11-times fan-out, the '0020E600'/"

```
003A98D0  mov      qword ptr [rsp + 8], rbx
003A98D5  push     rdi
003A98D6  sub      rsp, 0x20
003A98DA  mov      ebx, 8
003A98DF  xor      edi, edi
003A98E1  mov      rax, qword ptr [rip + 0x2b15690]  ; -> 02EBEF78
003A98E8  mov      rcx, qword ptr [rax]
003A98EB  mov      rcx, qword ptr [rbx + rcx]
003A98EF  test     rcx, rcx
003A98F2  je       0x3a9907  ; -> 003A9907
003A98F4  call     0x3697f0  ; -> 003697F0 fn
003A98F9  mov      rax, qword ptr [rip + 0x2b15678]  ; -> 02EBEF78
003A9900  mov      rcx, qword ptr [rax]
003A9903  mov      qword ptr [rbx + rcx], rdi
003A9907  add      rbx, 8
003A990B  cmp      rbx, 0x1800
003A9912  jl       0x3a98e1  ; -> 003A98E1
003A9914  mov      rbx, qword ptr [rsp + 0x30]
003A9919  add      rsp, 0x20
003A991D  pop      rdi
003A991E  ret      
```

## 003A99F0 (117 B, extent 003A99F0-003A9A65)

Page context: " ('0050050B'–'0050052F'), with a sub-range partner '00538910' for '0x42'–'0xAB' ('00538910'–'00538939'). '003A9A70' writes that byte and then calls it ('003A9A8F', '003A9AAD'). Its other callers are '003A99F0' (after a 'memcpy') and '003A9BA0', reached from the EFX data parse '003EDAD0' / '003ED8A0' and from instance creation '0024D540' / '0024D970'. **So it is the setup method**, run when an element is built. The step, update and walk "

```
003A99F0  mov      qword ptr [rsp + 8], rbx
003A99F5  mov      qword ptr [rsp + 0x10], rsi
003A99FA  push     rdi
003A99FB  sub      rsp, 0x20
003A99FF  movsx    eax, byte ptr [rcx + 2]
003A9A03  mov      rdi, rcx
003A9A06  movzx    ecx, word ptr [rcx]
003A9A09  movsxd   rbx, edx
003A9A0C  movzx    edx, ax
003A9A0F  mov      r8d, ebx
003A9A12  call     0x3a9ad0  ; -> 003A9AD0 fn
003A9A17  mov      rsi, rax
003A9A1A  test     rax, rax
003A9A1D  jne      0x3a9a2f  ; -> 003A9A2F
003A9A1F  mov      rbx, qword ptr [rsp + 0x30]
003A9A24  mov      rsi, qword ptr [rsp + 0x38]
003A9A29  add      rsp, 0x20
003A9A2D  pop      rdi
003A9A2E  ret      
003A9A2F  lea      rdx, [rdi + 4]
003A9A33  mov      r8, rbx
003A9A36  mov      rcx, rsi
003A9A39  call     0x861eba  ; -> 00861EBA fn
003A9A3E  mov      edx, dword ptr [rip + 0x2b11cf4]  ; -> 02EBB738
003A9A44  mov      rcx, rsi
003A9A47  add      edx, esi
003A9A49  call     0x5004c0  ; -> 005004C0 fn
003A9A4E  mov      rsi, qword ptr [rsp + 0x38]
003A9A53  lea      rax, [rdi + 4]
003A9A57  add      rax, rbx
003A9A5A  mov      rbx, qword ptr [rsp + 0x30]
003A9A5F  add      rsp, 0x20
003A9A63  pop      rdi
003A9A64  ret      
```

## 003CC0F0 (57 B, extent 003CC0F0-003CC129)

Page context: " ## SWE2-EC7-37 update (2026-09-19) - '003ED8A0'  '003ED8A0' (552 B) is the effect-file data parse - '02096D30'/'02096887'/'02096D34' (the effect camera), '003A9510'/'003A7CB0'/'003A75B0'/'0039D430'/'003CC0F0'/'003829D0'/'003A98D0'. Interior anchor '003ED909' (a '003A9510' call).  ## SWE2-EC7-37 update (2026-09-19) - '004352C0'  '004352C0' (537 B) is an element-record fill - '0020E600' 22-times/'003697F0' 11-times/'0020E620' 11-times fa"

```
003CC0F0  mov      qword ptr [rsp + 8], rbx
003CC0F5  push     rdi
003CC0F6  sub      rsp, 0x20
003CC0FA  mov      rbx, rcx
003CC0FD  mov      dword ptr [rcx + 0xc0], 0
003CC107  add      rcx, 0x20
003CC10B  mov      rdi, rdx
003CC10E  call     0x202c70  ; -> 00202C70 fn
003CC113  lea      rcx, [rbx + 0x60]
003CC117  mov      rdx, rdi
003CC11A  mov      rbx, qword ptr [rsp + 0x30]
003CC11F  add      rsp, 0x20
003CC123  pop      rdi
003CC124  jmp      0x202d50  ; -> 00202D50 fn
```

## 003D8E20 (41 B, extent 003D8E20-003D8E49)

Page context: "e row, the row's '+4' dword must equal 'ecx', and three dwords then copy from 'rdx' into '+0x10', '+0x14' and '+0x18' - key mismatch returns untouched; the value-update half of the parameter surface '003D8E20''s '+0x30' float write and '003D8D70''s '+0x3F' byte write sit beside.  Interior anchor '003D8E05' (function '003D8DE0').  '003D8D70' (41 B) is the sibling keyed byte store on '02B4D7D0': the same '(cl*3)*0x20' row selection and '+"

```
003D8E20  movzx    edx, cl
003D8E23  lea      rax, [rdx + rdx*2]
003D8E27  shl      rax, 5
003D8E2B  lea      rdx, [rip + 0x277499e]  ; -> 02B4D7D0
003D8E32  add      rax, rdx
003D8E35  xor      edx, edx
003D8E37  cmp      dword ptr [rax + 4], ecx
003D8E3A  cmovne   rax, rdx
003D8E3E  test     rax, rax
003D8E41  je       0x3d8e48  ; -> 003D8E48
003D8E43  movss    dword ptr [rax + 0x30], xmm1
003D8E48  ret      
```

## 003D9040 (119 B, extent 003D9040-003D90B7)

Page context: "003D8D70').  '003A3E20' (12 B) is the two-field record stamp half the dispatch's callers funnel through: 'dword[rcx+0x44]' sets to '-1' and 'word[rcx+0x42]' takes 'dx' - the invalidation+index write '003D9040', the '0045D'/'00522'/'0053' widget arms and '005386F0' all share before continuing their own tails.  Interior anchor '003A3E27' (function '003A3E20'). "

```
003D9040  push     rbx
003D9042  sub      rsp, 0x20
003D9046  xor      eax, eax
003D9048  mov      rbx, rcx
003D904B  mov      qword ptr [rcx + 0x330], rax
003D9052  mov      dword ptr [rcx + 0x338], eax
003D9058  call     0x2f2d60  ; -> 002F2D60 fn
003D905D  test     eax, eax
003D905F  jne      0x3d9067  ; -> 003D9067
003D9061  add      rsp, 0x20
003D9065  pop      rbx
003D9066  ret      
003D9067  lea      rcx, [rbx + 0x2d0]
003D906E  xor      edx, edx
003D9070  call     0x3a3e20  ; -> 003A3E20 fn
003D9075  mov      rcx, rbx
003D9078  call     0x3d92c0  ; -> 003D92C0 fn
003D907D  mov      rcx, qword ptr [rip + 0x2bbe2c4]  ; -> 02F97348
003D9084  cmp      byte ptr [rcx], 1
003D9087  jne      0x3d90ac  ; -> 003D90AC
003D9089  inc      byte ptr [rcx + 0x37a]
003D908F  mov      rcx, qword ptr [rip + 0x2bbe2b2]  ; -> 02F97348
003D9096  cmp      byte ptr [rcx + 0x37a], 1
003D909D  jne      0x3d90ac  ; -> 003D90AC
003D909F  mov      edx, 1
003D90A4  lea      ecx, [rdx + 2]
003D90A7  call     0x2ea8b0  ; -> 002EA8B0 fn
003D90AC  mov      eax, 1
003D90B1  add      rsp, 0x20
003D90B5  pop      rbx
003D90B6  ret      
```

## 003E7140 (198 B, extent 003E7140-003E7206)

Page context: "write or append through '+0x18'/'+0x10') - the effect family sibling of '003B4160''s '02B404E0' allocator.  Interior anchor '003771B6' (function '00377190').  '003D7FF0' (402 B) is the record issuer '003E7140'/'0047BE20' call on the '02B4D7D0' table (32 entries x 0x60, 'dword[+4]' occupied): 'byte[rcx+0xE]==2' + 'byte[02B4D7A2]' nonzero early-outs; '00181DD0' allocates into '+0x50', serial '02B4D7A4' packs '(serial<<8)|slot' into '+4', "

```
003E7140  push     rbx
003E7142  sub      rsp, 0x80
003E7149  movaps   xmmword ptr [rsp + 0x70], xmm6
003E714E  movaps   xmmword ptr [rsp + 0x60], xmm7
003E7153  movaps   xmmword ptr [rsp + 0x50], xmm8
003E7159  mov      rax, qword ptr [rip + 0x1b5d6d0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003E7160  xor      rax, rsp
003E7163  mov      qword ptr [rsp + 0x40], rax
003E7168  mov      rbx, rcx
003E716B  movaps   xmm8, xmm3
003E716F  mov      ecx, dword ptr [rcx + 0x448]
003E7175  movaps   xmm7, xmm2
003E7178  movaps   xmm6, xmm1
003E717B  test     ecx, ecx
003E717D  je       0x3e7184  ; -> 003E7184
003E717F  call     0x3d8300  ; -> 003D8300 fn
003E7184  mov      eax, dword ptr [rbx + 0x44c]
003E718A  xor      ecx, ecx
003E718C  and      byte ptr [rsp + 0x2d], 0x80
003E7191  mov      dword ptr [rbx + 0x448], eax
003E7197  movzx    eax, byte ptr [rsp + 0x2c]
003E719C  and      al, 0xc0
003E719E  movss    dword ptr [rsp + 0x20], xmm6
003E71A4  or       al, 0x40
003E71A6  movss    dword ptr [rsp + 0x24], xmm7
003E71AC  cmp      dword ptr [rsp + 0xb8], 4
003E71B4  movss    dword ptr [rsp + 0x28], xmm8
003E71BB  cmovl    ecx, dword ptr [rsp + 0xb8]
003E71C3  mov      dword ptr [rsp + 0x30], ecx
003E71C7  lea      rcx, [rsp + 0x20]
003E71CC  mov      byte ptr [rsp + 0x2c], al
003E71D0  mov      byte ptr [rsp + 0x2e], 2
003E71D5  call     0x3d7ff0  ; -> 003D7FF0 fn
003E71DA  mov      dword ptr [rbx + 0x44c], eax
003E71E0  mov      rcx, qword ptr [rsp + 0x40]
003E71E5  xor      rcx, rsp
003E71E8  call     0x808c40  ; -> 00808C40 fn
003E71ED  movaps   xmm6, xmmword ptr [rsp + 0x70]
003E71F2  movaps   xmm7, xmmword ptr [rsp + 0x60]
003E71F7  movaps   xmm8, xmmword ptr [rsp + 0x50]
003E71FD  add      rsp, 0x80
003E7204  pop      rbx
003E7205  ret      
```

## 00431040 (56 B, extent 00431040-00431078)

Page context: "90'/'0036DDA0' pair. Interior anchor '003A2993' (a '0036DD90' call).  ## SWE2-EC7-45 update (2026-09-19) - '00538B80'  '00538B80' (249 B) is an effect-element body - '0042FCF0'/'004304F0'/'00430AF0'/'00431040'/'00431580'/'00500470'. Interior anchor '00538B9E' (a '0042FCF0' call).  ## SWE2-EC7-47 update (2026-09-19) - '004354E0'  '004354E0' (219 B) is a body - '0020E620' single call. Interior anchor '004354F2' (the '0020E620' call).  ## "

```
00431040  push     rbx
00431042  sub      rsp, 0x30
00431046  movaps   xmmword ptr [rsp + 0x20], xmm6
0043104B  mov      rbx, rcx
0043104E  movaps   xmm6, xmm1
00431051  call     0x430a60  ; -> 00430A60 fn
00431056  lea      rcx, [rbx + 0x10]
0043105A  movaps   xmm1, xmm6
0043105D  call     0x430a60  ; -> 00430A60 fn
00431062  lea      rcx, [rbx + 0x20]
00431066  movaps   xmm1, xmm6
00431069  movaps   xmm6, xmmword ptr [rsp + 0x20]
0043106E  add      rsp, 0x30
00431072  pop      rbx
00431073  jmp      0x430a60  ; -> 00430A60 fn
```

## 0043E9C0 (89 B, extent 0043E9C0-0043EA19)

Page context: "by-frame.md) section 3 - over types '0x40'–'0xD1', called from '002F2530', '003A8DD0', '003A92D0' and '00442600'; and the five '0x42'-based sub-range tables, three of which — '0043EAB0', '0043ED30', '0043E9C0' — were found by the switch-family census and added the same day) and following each non-default arm to the function it jumps to or calls (['members/effect_type_methods.py'](members/effect_type_methods.py) → ['members/effect-type-m"

```
0043E9C0  movzx    eax, byte ptr [rcx]
0043E9C3  add      eax, -0x42
0043E9C6  cmp      eax, 0x61
0043E9C9  ja       0x43ea18  ; -> 0043EA18
0043E9CB  lea      r9, [rip - 0x31e9d2]  ; -> 00120000 (image base)
0043E9D2  cdqe     
0043E9D4  movzx    eax, byte ptr [r9 + rax + 0x31ea44]
0043E9DD  mov      r8d, dword ptr [r9 + rax*4 + 0x31ea1c]  ; image base + 0x31ea1c = 0043EA1C
0043E9E5  add      r8, r9
0043E9E8  jmp      r8
0043E9EB  jmp      0x524a10  ; -> 00524A10 fn
0043E9F0  jmp      0x526040  ; -> 00526040 fn
0043E9F5  jmp      0x16d6a0  ; -> 0016D6A0 fn
0043E9FA  jmp      0x47bf70  ; -> 0047BF70 fn
0043E9FF  jmp      0x5294b0  ; -> 005294B0 fn
0043EA04  jmp      0x52a340  ; -> 0052A340 fn
0043EA09  jmp      0x52b060  ; -> 0052B060 fn
0043EA0E  jmp      0x52d8e0  ; -> 0052D8E0 fn
0043EA13  jmp      0x52ea50  ; -> 0052EA50 fn
0043EA18  ret      
```

## 00448D70 (103 B, extent 00448D70-00448DD7)

Page context: "e, which is the tables. Types 1–5, for instance:  | type | step | update | walk | setup | |---|---|---|---|---| | '0x01' | '00442520' | '004424E0' | '00442550' | '00538A60' | | '0x02' | '00448DE0' | '00448D70' | '004490D0' | '00538AB0' | | '0x03' | '004427A0' | '00442760' | '004427D0' | '00538B80' | | '0x04' | '00445310' | '004452D0' | '004453D0' | '00538C80' | | '0x05' | '00449970' | '00449930' | '00449AB0' | '00538DB0' |  **What this "

```
00448D70  mov      qword ptr [rsp + 8], rbx
00448D75  push     rdi
00448D76  sub      rsp, 0x30
00448D7A  movaps   xmmword ptr [rsp + 0x20], xmm6
00448D7F  mov      rbx, rcx
00448D82  movaps   xmm6, xmm2
00448D85  call     0x2f2530  ; -> 002F2530 fn
00448D8A  mov      edi, eax
00448D8C  test     eax, eax
00448D8E  jne      0x448da0  ; -> 00448DA0
00448D90  mov      rbx, qword ptr [rsp + 0x40]
00448D95  movaps   xmm6, xmmword ptr [rsp + 0x20]
00448D9A  add      rsp, 0x30
00448D9E  pop      rdi
00448D9F  ret      
00448DA0  mov      rax, qword ptr [rbx + 0x20]
00448DA4  mov      ecx, 0x800
00448DA9  test     word ptr [rax + 0x180], cx
00448DB0  je       0x448dbd  ; -> 00448DBD
00448DB2  cvttss2si rax, xmm6
00448DB7  add      byte ptr [rbx + 0x2a1], al
00448DBD  mov      rcx, rbx
00448DC0  call     0x449560  ; -> 00449560 fn
00448DC5  mov      rbx, qword ptr [rsp + 0x40]
00448DCA  mov      eax, edi
00448DCC  movaps   xmm6, xmmword ptr [rsp + 0x20]
00448DD1  add      rsp, 0x30
00448DD5  pop      rdi
00448DD6  ret      
```

## 00455560 (1112 B, extent 00455560-004559B8)

Page context: "ical ladder shape to '0044E980' - the '0044DD00' arm's first stage.  Interior anchor '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call"

```
00455560  mov      qword ptr [rsp + 0x18], rbx
00455565  mov      qword ptr [rsp + 0x20], rdi
0045556A  push     rbp
0045556B  lea      rbp, [rsp - 0x57]
00455570  sub      rsp, 0x100
00455577  mov      rax, qword ptr [rip + 0x1aef2b2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045557E  xor      rax, rsp
00455581  mov      qword ptr [rbp + 0x47], rax
00455585  movups   xmm0, xmmword ptr [rcx + 0x250]
0045558C  mov      rdi, qword ptr [rcx + 0x20]
00455590  mov      rbx, rcx
00455593  movups   xmm1, xmmword ptr [rcx + 0x260]
0045559A  movups   xmmword ptr [rbp - 0x39], xmm0
0045559E  movups   xmm0, xmmword ptr [rcx + 0x270]
004555A5  movups   xmmword ptr [rbp - 0x29], xmm1
004555A9  movups   xmm1, xmmword ptr [rcx + 0x280]
004555B0  movups   xmmword ptr [rbp - 0x19], xmm0
004555B4  movups   xmmword ptr [rbp - 9], xmm1
004555B8  movzx    ecx, byte ptr [rdi + 0x4a]
004555BC  shr      ecx, 2
004555BF  and      ecx, 7
004555C2  sub      ecx, 1
004555C5  je       0x455603  ; -> 00455603
004555C7  sub      ecx, 1
004555CA  je       0x4555fa  ; -> 004555FA
004555CC  sub      ecx, 2
004555CF  je       0x4555e8  ; -> 004555E8
004555D1  cmp      ecx, 1
004555D4  jne      0x455613  ; -> 00455613
004555D6  lea      rcx, [rbp - 0x39]
004555DA  call     0x434a70  ; -> 00434A70 fn
004555DF  lea      rcx, [rip + 0x269947a]  ; -> 02AEEA60
004555E6  jmp      0x45560a  ; -> 0045560A
004555E8  lea      rcx, [rbp - 0x39]
004555EC  call     0x434900  ; -> 00434900 fn
004555F1  lea      rcx, [rip + 0x2699468]  ; -> 02AEEA60
004555F8  jmp      0x45560a  ; -> 0045560A
004555FA  lea      rcx, [rip + 0x269966f]  ; -> 02AEEC70
00455601  jmp      0x45560a  ; -> 0045560A
00455603  lea      rcx, [rip + 0x2699626]  ; -> 02AEEC30
0045560A  lea      rdx, [rbp - 0x39]
0045560E  call     0x398030  ; -> 00398030 fn
00455613  mov      ecx, dword ptr [rbx + 0x290]
00455619  call     0x39b620  ; -> 0039B620 fn
0045561E  lea      rcx, [rip + 0x269968b]  ; -> 02AEECB0
00455625  call     0x39b550  ; -> 0039B550 fn
0045562A  lea      rcx, [rbp + 7]
0045562E  call     0x3970a0  ; -> 003970A0 fn
00455633  lea      r8, [rip + 0x268acd6]  ; -> 02AE0310
0045563A  lea      rdx, [rbp - 0x39]
0045563E  lea      rcx, [rbp + 7]
00455642  call     0x397910  ; -> 00397910 fn
00455647  movzx    eax, byte ptr [rdi + 0x240]
0045564E  sub      al, 2
00455650  test     al, 0xfd
00455652  jne      0x455997  ; -> 00455997
00455658  mov      r9d, dword ptr [rbx + 0x44]
0045565C  lea      rdx, [rbp - 0x49]
00455660  xor      r8d, r8d
00455663  mov      qword ptr [rsp + 0x118], rsi
0045566B  lea      rcx, [rdi + 0x1a0]
00455672  call     0x431830  ; -> 00431830 fn
00455677  test     rax, rax
0045567A  je       0x45598f  ; -> 0045598F
00455680  mov      edx, dword ptr [rbx + 0x44]
00455683  lea      rcx, [rdi + 0x30]
00455687  call     0x4314e0  ; -> 004314E0 fn
0045568C  movsxd   rdx, eax
0045568F  lea      rcx, [rdi + 0x1a0]
00455696  movzx    eax, word ptr [rdi + 0x24a]
0045569D  and      eax, 7
004556A0  mov      qword ptr [rip + 0x2699261], rdx  ; -> 02AEE908
004556A7  mov      dword ptr [rip + 0x2699253], eax  ; -> 02AEE900
004556AD  mov      rax, qword ptr [rbp - 0x49]
004556B1  mov      qword ptr [rip + 0x268acb8], rax  ; -> 02AE0370
004556B8  mov      rax, qword ptr [rbp - 0x41]
004556BC  mov      qword ptr [rip + 0x268ac9d], rax  ; -> 02AE0360
004556C3  mov      edx, dword ptr [rbx + 0x44]
004556C6  call     0x4309c0  ; -> 004309C0 fn
004556CB  movss    dword ptr [rip + 0x268abdd], xmm0  ; -> 02AE02B0
004556D3  lea      rcx, [rdi + 0x1b0]
004556DA  mov      edx, dword ptr [rbx + 0x44]
004556DD  call     0x4309c0  ; -> 004309C0 fn
004556E2  movss    xmm1, dword ptr [rip + 0x268abc6]  ; -> 02AE02B0
004556EA  lea      rsi, [rbx + 0x230]
004556F1  movss    dword ptr [rip + 0x268abbb], xmm0  ; -> 02AE02B4
004556F9  lea      r8, [rbp - 0x65]
004556FD  addss    xmm1, dword ptr [rbx + 0x29c]
00455705  mov      rdx, rsi
00455708  mov      rcx, rbx
0045570B  movss    dword ptr [rip + 0x268ab9d], xmm1  ; -> 02AE02B0
00455713  addss    xmm0, dword ptr [rbx + 0x2a0]
0045571B  movss    dword ptr [rip + 0x268ab91], xmm0  ; -> 02AE02B4
00455723  call     0x2f1f40  ; -> 002F1F40 fn
00455728  lea      rdx, [rbx + 0x240]
0045572F  lea      r8, [rbp - 0x65]
00455733  lea      rcx, [rbp - 0x65]
00455737  call     0x26ee00  ; -> 0026EE00 fn
0045573C  mov      edx, dword ptr [rbx + 0x44]
0045573F  lea      rcx, [rdi + 0x1e0]
00455746  call     0x42fdb0  ; -> 0042FDB0 fn
0045574B  lea      r8, [rbp - 0x65]
0045574F  mov      dword ptr [rbp - 0x69], eax
00455752  lea      rdx, [rbp - 0x69]
00455756  lea      rcx, [rbp - 0x69]
0045575A  call     0x26ee00  ; -> 0026EE00 fn
0045575F  movzx    eax, byte ptr [rbp - 0x69]
00455763  mov      dword ptr [rip + 0x268ab37], eax  ; -> 02AE02A0
00455769  movzx    eax, byte ptr [rbp - 0x68]
0045576D  mov      dword ptr [rip + 0x268ab31], eax  ; -> 02AE02A4
00455773  movzx    eax, byte ptr [rbp - 0x67]
00455777  mov      dword ptr [rip + 0x268ab2b], eax  ; -> 02AE02A8
0045577D  movzx    eax, byte ptr [rbp - 0x66]
00455781  mov      dword ptr [rip + 0x268ab25], eax  ; -> 02AE02AC
00455787  movsxd   rax, dword ptr [rbx + 0x298]
0045578E  mov      ecx, dword ptr [rdi + rax*4 + 0x2a0]
00455795  call     0x20e600  ; -> 0020E600 fn
0045579A  mov      rbx, rax
0045579D  test     rax, rax
004557A0  je       0x45598f  ; -> 0045598F
004557A6  lea      rcx, [rip + 0x2699503]  ; -> 02AEECB0
004557AD  call     0x39b550  ; -> 0039B550 fn
004557B2  movzx    edx, byte ptr [rdi + 0x294]
004557B9  shr      edx, 1
004557BB  and      edx, 3
004557BE  sub      edx, 1
004557C1  je       0x4558da  ; -> 004558DA
004557C7  sub      edx, 1
004557CA  je       0x4558ce  ; -> 004558CE
004557D0  cmp      edx, 1
004557D3  jne      0x45598f  ; -> 0045598F
004557D9  test     byte ptr [rdi + 0x24a], 7
004557E0  jne      0x455844  ; -> 00455844
004557E2  mov      dword ptr [rip + 0x268aa94], 2  ; -> 02AE0280
004557EC  mov      ecx, dword ptr [rbx + 0x10]
004557EF  call     0x20e600  ; -> 0020E600 fn
004557F4  mov      ecx, dword ptr [rbx + 0x14]
004557F7  lea      rdi, [rip + 0x268aa7a]  ; -> 02AE0278
004557FE  mov      edx, dword ptr [rip + 0x268aa68]  ; -> 02AE026C
00455804  lea      r8, [rip + 0x44215]  ; -> 00499A20
0045580B  mov      dword ptr [rsp + 0x30], ecx
0045580F  mov      r9, rdi
00455812  mov      ecx, dword ptr [rip + 0x268aa50]  ; -> 02AE0268
00455818  mov      qword ptr [rsp + 0x28], rax
0045581D  mov      dword ptr [rsp + 0x20], 0x118
00455825  call     0x3a2f70  ; -> 003A2F70 fn
0045582A  mov      dword ptr [rip + 0x268aa4c], 0  ; -> 02AE0280
00455834  mov      ecx, dword ptr [rbx + 0x10]
00455837  call     0x20e600  ; -> 0020E600 fn
0045583C  mov      r9, rdi
0045583F  jmp      0x4558fc  ; -> 004558FC
00455844  test     byte ptr [rdi + 0x4b], 1
00455848  mov      rcx, rsi
0045584B  jne      0x455863  ; -> 00455863
0045584D  lea      rdx, [rbp - 0x59]
00455851  call     0x399600  ; -> 00399600 fn
00455856  test     eax, eax
00455858  jne      0x45598f  ; -> 0045598F
0045585E  mov      esi, dword ptr [rbp - 0x55]
00455861  jmp      0x45586a  ; -> 0045586A
00455863  call     0x39a9b0  ; -> 0039A9B0 fn
00455868  mov      esi, eax
0045586A  mov      dword ptr [rip + 0x268aa0c], 2  ; -> 02AE0280
00455874  mov      ecx, dword ptr [rbx + 0x10]
00455877  call     0x20e600  ; -> 0020E600 fn
0045587C  mov      ecx, dword ptr [rbx + 0x14]
0045587F  lea      rdi, [rip + 0x268a9f2]  ; -> 02AE0278
00455886  mov      r8d, dword ptr [rip + 0x268a9df]  ; -> 02AE026C
0045588D  lea      r9, [rip + 0x4418c]  ; -> 00499A20
00455894  mov      edx, dword ptr [rip + 0x268a9ce]  ; -> 02AE0268
0045589A  mov      dword ptr [rsp + 0x38], ecx
0045589E  mov      ecx, esi
004558A0  mov      qword ptr [rsp + 0x30], rax
004558A5  mov      dword ptr [rsp + 0x28], 0x118
004558AD  mov      qword ptr [rsp + 0x20], rdi
004558B2  call     0x3a33b0  ; -> 003A33B0 fn
004558B7  mov      dword ptr [rip + 0x268a9bf], 0  ; -> 02AE0280
004558C1  mov      ecx, dword ptr [rbx + 0x10]
004558C4  call     0x20e600  ; -> 0020E600 fn
004558C9  jmp      0x45595b  ; -> 0045595B
004558CE  mov      dword ptr [rip + 0x268a9a8], 2  ; -> 02AE0280
004558D8  jmp      0x4558e4  ; -> 004558E4
004558DA  mov      dword ptr [rip + 0x268a99c], 0  ; -> 02AE0280
004558E4  test     byte ptr [rdi + 0x24a], 7
004558EB  jne      0x45592a  ; -> 0045592A
004558ED  mov      ecx, dword ptr [rbx + 0x10]
004558F0  call     0x20e600  ; -> 0020E600 fn
004558F5  lea      r9, [rip + 0x268a97c]  ; -> 02AE0278
004558FC  mov      ecx, dword ptr [rbx + 0x14]
004558FF  lea      r8, [rip + 0x4411a]  ; -> 00499A20
00455906  mov      edx, dword ptr [rip + 0x268a960]  ; -> 02AE026C
0045590C  mov      dword ptr [rsp + 0x30], ecx
00455910  mov      ecx, dword ptr [rip + 0x268a952]  ; -> 02AE0268
00455916  mov      qword ptr [rsp + 0x28], rax
0045591B  mov      dword ptr [rsp + 0x20], 0x118
00455923  call     0x3a2f70  ; -> 003A2F70 fn
00455928  jmp      0x45598f  ; -> 0045598F
0045592A  test     byte ptr [rdi + 0x4b], 1
0045592E  mov      rcx, rsi
00455931  jne      0x455945  ; -> 00455945
00455933  lea      rdx, [rbp - 0x59]
00455937  call     0x399600  ; -> 00399600 fn
0045593C  test     eax, eax
0045593E  jne      0x45598f  ; -> 0045598F
00455940  mov      esi, dword ptr [rbp - 0x55]
00455943  jmp      0x45594c  ; -> 0045594C
00455945  call     0x39a9b0  ; -> 0039A9B0 fn
0045594A  mov      esi, eax
0045594C  mov      ecx, dword ptr [rbx + 0x10]
0045594F  call     0x20e600  ; -> 0020E600 fn
00455954  lea      rdi, [rip + 0x268a91d]  ; -> 02AE0278
0045595B  mov      ecx, dword ptr [rbx + 0x14]
0045595E  lea      r9, [rip + 0x440bb]  ; -> 00499A20
00455965  mov      r8d, dword ptr [rip + 0x268a900]  ; -> 02AE026C
0045596C  mov      edx, dword ptr [rip + 0x268a8f6]  ; -> 02AE0268
00455972  mov      dword ptr [rsp + 0x38], ecx
00455976  mov      ecx, esi
00455978  mov      qword ptr [rsp + 0x30], rax
0045597D  mov      dword ptr [rsp + 0x28], 0x118
00455985  mov      qword ptr [rsp + 0x20], rdi
0045598A  call     0x3a33b0  ; -> 003A33B0 fn
0045598F  mov      rsi, qword ptr [rsp + 0x118]
00455997  mov      rcx, qword ptr [rbp + 0x47]
0045599B  xor      rcx, rsp
0045599E  call     0x808c40  ; -> 00808C40 fn
004559A3  lea      r11, [rsp + 0x100]
004559AB  mov      rbx, qword ptr [r11 + 0x20]
004559AF  mov      rdi, qword ptr [r11 + 0x28]
004559B3  mov      rsp, r11
004559B6  pop      rbp
004559B7  ret      
```

## 004559C0 (870 B, extent 004559C0-00455D26)

Page context: "shape to '0044E980' - the '0044DD00' arm's first stage.  Interior anchor '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call field step."

```
004559C0  push     rbp
004559C2  push     rbx
004559C3  push     rdi
004559C4  lea      rbp, [rsp - 0x47]
004559C9  sub      rsp, 0x100
004559D0  mov      rax, qword ptr [rip + 0x1aeee59]  ; -> 01F44830 [u64 0x00002B992DDFA232]
004559D7  xor      rax, rsp
004559DA  mov      qword ptr [rbp + 0x37], rax
004559DE  movups   xmm0, xmmword ptr [rcx + 0x250]
004559E5  mov      rbx, qword ptr [rcx + 0x20]
004559E9  mov      rdi, rcx
004559EC  movups   xmm1, xmmword ptr [rcx + 0x260]
004559F3  movups   xmmword ptr [rbp - 0x59], xmm0
004559F7  movups   xmm0, xmmword ptr [rcx + 0x270]
004559FE  movups   xmmword ptr [rbp - 0x49], xmm1
00455A02  movups   xmm1, xmmword ptr [rcx + 0x280]
00455A09  movups   xmmword ptr [rbp - 0x39], xmm0
00455A0D  movups   xmmword ptr [rbp - 0x29], xmm1
00455A11  movzx    ecx, byte ptr [rbx + 0x4a]
00455A15  shr      ecx, 2
00455A18  and      ecx, 7
00455A1B  sub      ecx, 1
00455A1E  je       0x455a5c  ; -> 00455A5C
00455A20  sub      ecx, 1
00455A23  je       0x455a53  ; -> 00455A53
00455A25  sub      ecx, 2
00455A28  je       0x455a41  ; -> 00455A41
00455A2A  cmp      ecx, 1
00455A2D  jne      0x455a6c  ; -> 00455A6C
00455A2F  lea      rcx, [rbp - 0x59]
00455A33  call     0x434a70  ; -> 00434A70 fn
00455A38  lea      rcx, [rip + 0x2699021]  ; -> 02AEEA60
00455A3F  jmp      0x455a63  ; -> 00455A63
00455A41  lea      rcx, [rbp - 0x59]
00455A45  call     0x434900  ; -> 00434900 fn
00455A4A  lea      rcx, [rip + 0x269900f]  ; -> 02AEEA60
00455A51  jmp      0x455a63  ; -> 00455A63
00455A53  lea      rcx, [rip + 0x2699216]  ; -> 02AEEC70
00455A5A  jmp      0x455a63  ; -> 00455A63
00455A5C  lea      rcx, [rip + 0x26991cd]  ; -> 02AEEC30
00455A63  lea      rdx, [rbp - 0x59]
00455A67  call     0x398030  ; -> 00398030 fn
00455A6C  mov      ecx, dword ptr [rdi + 0x290]
00455A72  call     0x39b620  ; -> 0039B620 fn
00455A77  lea      rcx, [rip + 0x2699232]  ; -> 02AEECB0
00455A7E  call     0x39b550  ; -> 0039B550 fn
00455A83  lea      rcx, [rbp - 9]
00455A87  call     0x3970a0  ; -> 003970A0 fn
00455A8C  lea      r8, [rip + 0x268a74d]  ; -> 02AE01E0
00455A93  lea      rdx, [rbp - 0x59]
00455A97  lea      rcx, [rbp - 9]
00455A9B  call     0x397910  ; -> 00397910 fn
00455AA0  movzx    eax, byte ptr [rbx + 0x240]
00455AA7  sub      al, 2
00455AA9  test     al, 0xfd
00455AAB  jne      0x455d0f  ; -> 00455D0F
00455AB1  mov      r9d, dword ptr [rdi + 0x44]
00455AB5  lea      rdx, [rbp - 0x69]
00455AB9  xor      r8d, r8d
00455ABC  mov      qword ptr [rsp + 0x128], rsi
00455AC4  lea      rcx, [rbx + 0x1a0]
00455ACB  call     0x431830  ; -> 00431830 fn
00455AD0  test     rax, rax
00455AD3  je       0x455d07  ; -> 00455D07
00455AD9  mov      edx, dword ptr [rdi + 0x44]
00455ADC  lea      rcx, [rbx + 0x30]
00455AE0  mov      qword ptr [rsp + 0x130], r14
00455AE8  call     0x4314e0  ; -> 004314E0 fn
00455AED  movsxd   rdx, eax
00455AF0  lea      rcx, [rbx + 0x1a0]
00455AF7  movzx    eax, word ptr [rbx + 0x24a]
00455AFE  and      eax, 7
00455B01  mov      qword ptr [rip + 0x2698e00], rdx  ; -> 02AEE908
00455B08  mov      dword ptr [rip + 0x2698df2], eax  ; -> 02AEE900
00455B0E  mov      rax, qword ptr [rbp - 0x69]
00455B12  mov      qword ptr [rip + 0x268a727], rax  ; -> 02AE0240
00455B19  mov      rax, qword ptr [rbp - 0x61]
00455B1D  mov      qword ptr [rip + 0x268a70c], rax  ; -> 02AE0230
00455B24  mov      edx, dword ptr [rdi + 0x44]
00455B27  call     0x4309c0  ; -> 004309C0 fn
00455B2C  movss    dword ptr [rip + 0x268a64c], xmm0  ; -> 02AE0180
00455B34  lea      rcx, [rbx + 0x1b0]
00455B3B  mov      edx, dword ptr [rdi + 0x44]
00455B3E  call     0x4309c0  ; -> 004309C0 fn
00455B43  movss    xmm1, dword ptr [rip + 0x268a635]  ; -> 02AE0180
00455B4B  lea      r8, [rbp - 0x75]
00455B4F  movss    dword ptr [rip + 0x268a62d], xmm0  ; -> 02AE0184
00455B57  lea      rdx, [rdi + 0x230]
00455B5E  addss    xmm1, dword ptr [rdi + 0x29c]
00455B66  mov      rcx, rdi
00455B69  movss    dword ptr [rip + 0x268a60f], xmm1  ; -> 02AE0180
00455B71  addss    xmm0, dword ptr [rdi + 0x2a0]
00455B79  movss    dword ptr [rip + 0x268a603], xmm0  ; -> 02AE0184
00455B81  call     0x2f1f40  ; -> 002F1F40 fn
00455B86  lea      rdx, [rdi + 0x240]
00455B8D  lea      r8, [rbp - 0x75]
00455B91  lea      rcx, [rbp - 0x75]
00455B95  call     0x26ee00  ; -> 0026EE00 fn
00455B9A  mov      edx, dword ptr [rdi + 0x44]
00455B9D  lea      rcx, [rbx + 0x1e0]
00455BA4  call     0x42fdb0  ; -> 0042FDB0 fn
00455BA9  lea      r8, [rbp - 0x75]
00455BAD  mov      dword ptr [rbp - 0x79], eax
00455BB0  lea      rdx, [rbp - 0x79]
00455BB4  lea      rcx, [rbp - 0x79]
00455BB8  call     0x26ee00  ; -> 0026EE00 fn
00455BBD  movzx    eax, byte ptr [rbp - 0x79]
00455BC1  mov      dword ptr [rip + 0x268a5a9], eax  ; -> 02AE0170
00455BC7  movzx    eax, byte ptr [rbp - 0x78]
00455BCB  mov      dword ptr [rip + 0x268a5a3], eax  ; -> 02AE0174
00455BD1  movzx    eax, byte ptr [rbp - 0x77]
00455BD5  mov      dword ptr [rip + 0x268a59d], eax  ; -> 02AE0178
00455BDB  movzx    eax, byte ptr [rbp - 0x76]
00455BDF  mov      dword ptr [rip + 0x268a597], eax  ; -> 02AE017C
00455BE5  movsxd   rax, dword ptr [rdi + 0x298]
00455BEC  mov      ecx, dword ptr [rbx + rax*4 + 0x2a0]
00455BF3  call     0x20e600  ; -> 0020E600 fn
00455BF8  mov      rsi, rax
00455BFB  test     rax, rax
00455BFE  je       0x455cff  ; -> 00455CFF
00455C04  test     byte ptr [rbx + 0x24a], 7
00455C0B  jne      0x455c5a  ; -> 00455C5A
00455C0D  mov      rcx, qword ptr [rdi + 0x20]
00455C11  movzx    ecx, byte ptr [rcx + 0x74]
00455C15  call     0x3a3d00  ; -> 003A3D00 fn
00455C1A  mov      ecx, dword ptr [rsi + 0x10]
00455C1D  call     0x20e600  ; -> 0020E600 fn
00455C22  mov      ecx, dword ptr [rsi + 0x14]
00455C25  lea      r9, [rip + 0x268a51c]  ; -> 02AE0148
00455C2C  mov      edx, dword ptr [rip + 0x268a50a]  ; -> 02AE013C
00455C32  lea      r8, [rip + 0x41e87]  ; -> 00497AC0
00455C39  mov      dword ptr [rsp + 0x30], ecx
00455C3D  mov      ecx, dword ptr [rip + 0x268a4f5]  ; -> 02AE0138
00455C43  mov      qword ptr [rsp + 0x28], rax
00455C48  mov      dword ptr [rsp + 0x20], 0x118
00455C50  call     0x3a2f70  ; -> 003A2F70 fn
00455C55  jmp      0x455cf8  ; -> 00455CF8
00455C5A  lea      rcx, [rip + 0x269904f]  ; -> 02AEECB0
00455C61  call     0x39b550  ; -> 0039B550 fn
00455C66  test     byte ptr [rbx + 0x4b], 1
00455C6A  lea      rcx, [rdi + 0x230]
00455C71  jne      0x455ca1  ; -> 00455CA1
00455C73  lea      rdx, [rbp - 0x19]
00455C77  call     0x399600  ; -> 00399600 fn
00455C7C  test     eax, eax
00455C7E  jne      0x455cff  ; -> 00455CFF
00455C80  mov      rax, qword ptr [rdi + 0x20]
00455C84  movzx    ecx, byte ptr [rax + 0x74]
00455C88  call     0x3a3d00  ; -> 003A3D00 fn
00455C8D  mov      ecx, dword ptr [rsi + 0x10]
00455C90  call     0x20e600  ; -> 0020E600 fn
00455C95  mov      ecx, dword ptr [rsi + 0x14]
00455C98  mov      dword ptr [rsp + 0x38], ecx
00455C9C  mov      ecx, dword ptr [rbp - 0x15]
00455C9F  jmp      0x455cc6  ; -> 00455CC6
00455CA1  call     0x39a9b0  ; -> 0039A9B0 fn
00455CA6  mov      rcx, qword ptr [rdi + 0x20]
00455CAA  mov      ebx, eax
00455CAC  movzx    ecx, byte ptr [rcx + 0x74]
00455CB0  call     0x3a3d00  ; -> 003A3D00 fn
00455CB5  mov      ecx, dword ptr [rsi + 0x10]
00455CB8  call     0x20e600  ; -> 0020E600 fn
00455CBD  mov      ecx, dword ptr [rsi + 0x14]
00455CC0  mov      dword ptr [rsp + 0x38], ecx
00455CC4  mov      ecx, ebx
00455CC6  mov      r8d, dword ptr [rip + 0x268a46f]  ; -> 02AE013C
00455CCD  lea      r9, [rip + 0x41dec]  ; -> 00497AC0
00455CD4  mov      edx, dword ptr [rip + 0x268a45e]  ; -> 02AE0138
00455CDA  mov      qword ptr [rsp + 0x30], rax
00455CDF  lea      rax, [rip + 0x268a462]  ; -> 02AE0148
00455CE6  mov      dword ptr [rsp + 0x28], 0x118
00455CEE  mov      qword ptr [rsp + 0x20], rax
00455CF3  call     0x3a33b0  ; -> 003A33B0 fn
00455CF8  xor      ecx, ecx
00455CFA  call     0x3a3d00  ; -> 003A3D00 fn
00455CFF  mov      r14, qword ptr [rsp + 0x130]
00455D07  mov      rsi, qword ptr [rsp + 0x128]
00455D0F  mov      rcx, qword ptr [rbp + 0x37]
00455D13  xor      rcx, rsp
00455D16  call     0x808c40  ; -> 00808C40 fn
00455D1B  add      rsp, 0x100
00455D22  pop      rdi
00455D23  pop      rbx
00455D24  pop      rbp
00455D25  ret      
```

## 0045A220 (1152 B, extent 0045A220-0045A6A0)

Page context: " arm's first stage.  Interior anchor '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call field step.  Interior anchor '003A2F94' (functi"

```
0045A220  mov      qword ptr [rsp + 0x20], rbx
0045A225  push     rbp
0045A226  lea      rbp, [rsp - 0x57]
0045A22B  sub      rsp, 0x100
0045A232  mov      rax, qword ptr [rip + 0x1aea5f7]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045A239  xor      rax, rsp
0045A23C  mov      qword ptr [rbp + 0x47], rax
0045A240  cmp      byte ptr [rcx], 0
0045A243  mov      rbx, rcx
0045A246  je       0x45a683  ; -> 0045A683
0045A24C  movups   xmm0, xmmword ptr [rcx + 0x250]
0045A253  mov      qword ptr [rsp + 0x120], rdi
0045A25B  movups   xmm1, xmmword ptr [rcx + 0x260]
0045A262  mov      rdi, qword ptr [rcx + 0x20]
0045A266  movups   xmmword ptr [rbp - 0x39], xmm0
0045A26A  movups   xmm0, xmmword ptr [rcx + 0x270]
0045A271  movups   xmmword ptr [rbp - 0x29], xmm1
0045A275  movups   xmm1, xmmword ptr [rcx + 0x280]
0045A27C  movups   xmmword ptr [rbp - 0x19], xmm0
0045A280  movups   xmmword ptr [rbp - 9], xmm1
0045A284  movzx    ecx, byte ptr [rdi + 0x4a]
0045A288  shr      ecx, 2
0045A28B  and      ecx, 7
0045A28E  sub      ecx, 1
0045A291  je       0x45a2cf  ; -> 0045A2CF
0045A293  sub      ecx, 1
0045A296  je       0x45a2c6  ; -> 0045A2C6
0045A298  sub      ecx, 2
0045A29B  je       0x45a2b4  ; -> 0045A2B4
0045A29D  cmp      ecx, 1
0045A2A0  jne      0x45a2df  ; -> 0045A2DF
0045A2A2  lea      rcx, [rbp - 0x39]
0045A2A6  call     0x434a70  ; -> 00434A70 fn
0045A2AB  lea      rcx, [rip + 0x26947ae]  ; -> 02AEEA60
0045A2B2  jmp      0x45a2d6  ; -> 0045A2D6
0045A2B4  lea      rcx, [rbp - 0x39]
0045A2B8  call     0x434900  ; -> 00434900 fn
0045A2BD  lea      rcx, [rip + 0x269479c]  ; -> 02AEEA60
0045A2C4  jmp      0x45a2d6  ; -> 0045A2D6
0045A2C6  lea      rcx, [rip + 0x26949a3]  ; -> 02AEEC70
0045A2CD  jmp      0x45a2d6  ; -> 0045A2D6
0045A2CF  lea      rcx, [rip + 0x269495a]  ; -> 02AEEC30
0045A2D6  lea      rdx, [rbp - 0x39]
0045A2DA  call     0x398030  ; -> 00398030 fn
0045A2DF  mov      ecx, dword ptr [rbx + 0x290]
0045A2E5  call     0x39b620  ; -> 0039B620 fn
0045A2EA  lea      rcx, [rip + 0x26949bf]  ; -> 02AEECB0
0045A2F1  call     0x39b550  ; -> 0039B550 fn
0045A2F6  lea      rcx, [rbp + 7]
0045A2FA  call     0x3970a0  ; -> 003970A0 fn
0045A2FF  lea      r8, [rip + 0x2688d1a]  ; -> 02AE3020
0045A306  lea      rdx, [rbp - 0x39]
0045A30A  lea      rcx, [rbp + 7]
0045A30E  call     0x397910  ; -> 00397910 fn
0045A313  movzx    eax, byte ptr [rdi + 0x250]
0045A31A  sub      al, 2
0045A31C  test     al, 0xfd
0045A31E  jne      0x45a67b  ; -> 0045A67B
0045A324  mov      r9d, dword ptr [rbx + 0x44]
0045A328  lea      rdx, [rbp - 0x49]
0045A32C  xor      r8d, r8d
0045A32F  mov      qword ptr [rsp + 0x118], rsi
0045A337  lea      rcx, [rdi + 0x1b0]
0045A33E  call     0x431830  ; -> 00431830 fn
0045A343  test     rax, rax
0045A346  je       0x45a673  ; -> 0045A673
0045A34C  mov      edx, dword ptr [rbx + 0x44]
0045A34F  lea      rcx, [rdi + 0x30]
0045A353  call     0x4314e0  ; -> 004314E0 fn
0045A358  movsxd   rdx, eax
0045A35B  lea      rcx, [rdi + 0x1b0]
0045A362  movzx    eax, word ptr [rdi + 0x25a]
0045A369  and      eax, 7
0045A36C  mov      qword ptr [rip + 0x2694595], rdx  ; -> 02AEE908
0045A373  mov      dword ptr [rip + 0x2694587], eax  ; -> 02AEE900
0045A379  mov      rax, qword ptr [rbp - 0x41]
0045A37D  mov      qword ptr [rip + 0x2688cec], rax  ; -> 02AE3070
0045A384  mov      rax, qword ptr [rbp - 0x49]
0045A388  mov      qword ptr [rip + 0x2688cf1], rax  ; -> 02AE3080
0045A38F  mov      edx, dword ptr [rbx + 0x44]
0045A392  call     0x4309c0  ; -> 004309C0 fn
0045A397  movss    dword ptr [rip + 0x2688c21], xmm0  ; -> 02AE2FC0
0045A39F  lea      rcx, [rdi + 0x1c0]
0045A3A6  mov      edx, dword ptr [rbx + 0x44]
0045A3A9  call     0x4309c0  ; -> 004309C0 fn
0045A3AE  movss    xmm1, dword ptr [rip + 0x2688c0a]  ; -> 02AE2FC0
0045A3B6  lea      rsi, [rbx + 0x230]
0045A3BD  movss    dword ptr [rip + 0x2688bff], xmm0  ; -> 02AE2FC4
0045A3C5  lea      r8, [rbp - 0x65]
0045A3C9  addss    xmm1, dword ptr [rbx + 0x29c]
0045A3D1  mov      rdx, rsi
0045A3D4  mov      rcx, rbx
0045A3D7  movss    dword ptr [rip + 0x2688be1], xmm1  ; -> 02AE2FC0
0045A3DF  addss    xmm0, dword ptr [rbx + 0x2a0]
0045A3E7  movss    dword ptr [rip + 0x2688bd5], xmm0  ; -> 02AE2FC4
0045A3EF  call     0x2f1f40  ; -> 002F1F40 fn
0045A3F4  lea      rdx, [rbx + 0x240]
0045A3FB  lea      r8, [rbp - 0x65]
0045A3FF  lea      rcx, [rbp - 0x65]
0045A403  call     0x26ee00  ; -> 0026EE00 fn
0045A408  mov      edx, dword ptr [rbx + 0x44]
0045A40B  lea      rcx, [rdi + 0x1f0]
0045A412  call     0x42fdb0  ; -> 0042FDB0 fn
0045A417  lea      r8, [rbp - 0x65]
0045A41B  mov      dword ptr [rbp - 0x69], eax
0045A41E  lea      rdx, [rbp - 0x69]
0045A422  lea      rcx, [rbp - 0x69]
0045A426  call     0x26ee00  ; -> 0026EE00 fn
0045A42B  movzx    eax, byte ptr [rbp - 0x69]
0045A42F  lea      rcx, [rdi + 0x190]
0045A436  mov      dword ptr [rip + 0x2688b74], eax  ; -> 02AE2FB0
0045A43C  movzx    eax, byte ptr [rbp - 0x68]
0045A440  mov      dword ptr [rip + 0x2688b6e], eax  ; -> 02AE2FB4
0045A446  movzx    eax, byte ptr [rbp - 0x67]
0045A44A  mov      dword ptr [rip + 0x2688b68], eax  ; -> 02AE2FB8
0045A450  movzx    eax, byte ptr [rbp - 0x66]
0045A454  mov      dword ptr [rip + 0x2688b62], eax  ; -> 02AE2FBC
0045A45A  mov      edx, dword ptr [rbx + 0x44]
0045A45D  call     0x4309c0  ; -> 004309C0 fn
0045A462  movss    dword ptr [rip + 0x2688b62], xmm0  ; -> 02AE2FCC
0045A46A  movsxd   rax, dword ptr [rbx + 0x298]
0045A471  mov      ecx, dword ptr [rdi + rax*4 + 0x2b0]
0045A478  call     0x20e600  ; -> 0020E600 fn
0045A47D  mov      rbx, rax
0045A480  test     rax, rax
0045A483  je       0x45a673  ; -> 0045A673
0045A489  lea      rcx, [rip + 0x2694820]  ; -> 02AEECB0
0045A490  call     0x39b550  ; -> 0039B550 fn
0045A495  movzx    ecx, byte ptr [rdi + 0x2a4]
0045A49C  shr      cl, 1
0045A49E  and      cl, 3
0045A4A1  movzx    eax, cl
0045A4A4  cmp      cl, 1
0045A4A7  jbe      0x45a5be  ; -> 0045A5BE
0045A4AD  cmp      al, 2
0045A4AF  je       0x45a5b2  ; -> 0045A5B2
0045A4B5  cmp      al, 3
0045A4B7  jne      0x45a673  ; -> 0045A673
0045A4BD  test     byte ptr [rdi + 0x25a], 7
0045A4C4  jne      0x45a528  ; -> 0045A528
0045A4C6  mov      dword ptr [rip + 0x2688ac0], 2  ; -> 02AE2F90
0045A4D0  mov      ecx, dword ptr [rbx + 0x10]
0045A4D3  call     0x20e600  ; -> 0020E600 fn
0045A4D8  mov      ecx, dword ptr [rbx + 0x14]
0045A4DB  lea      rdi, [rip + 0x2688aa6]  ; -> 02AE2F88
0045A4E2  mov      edx, dword ptr [rip + 0x2688a94]  ; -> 02AE2F7C
0045A4E8  lea      r8, [rip + 0x50ad1]  ; -> 004AAFC0
0045A4EF  mov      dword ptr [rsp + 0x30], ecx
0045A4F3  mov      r9, rdi
0045A4F6  mov      ecx, dword ptr [rip + 0x2688a7c]  ; -> 02AE2F78
0045A4FC  mov      qword ptr [rsp + 0x28], rax
0045A501  mov      dword ptr [rsp + 0x20], 0x118
0045A509  call     0x3a2f70  ; -> 003A2F70 fn
0045A50E  mov      dword ptr [rip + 0x2688a78], 0  ; -> 02AE2F90
0045A518  mov      ecx, dword ptr [rbx + 0x10]
0045A51B  call     0x20e600  ; -> 0020E600 fn
0045A520  mov      r9, rdi
0045A523  jmp      0x45a5e0  ; -> 0045A5E0
0045A528  test     byte ptr [rdi + 0x4b], 1
0045A52C  mov      rcx, rsi
0045A52F  jne      0x45a547  ; -> 0045A547
0045A531  lea      rdx, [rbp - 0x59]
0045A535  call     0x399600  ; -> 00399600 fn
0045A53A  test     eax, eax
0045A53C  jne      0x45a673  ; -> 0045A673
0045A542  mov      esi, dword ptr [rbp - 0x55]
0045A545  jmp      0x45a54e  ; -> 0045A54E
0045A547  call     0x39a9b0  ; -> 0039A9B0 fn
0045A54C  mov      esi, eax
0045A54E  mov      dword ptr [rip + 0x2688a38], 2  ; -> 02AE2F90
0045A558  mov      ecx, dword ptr [rbx + 0x10]
0045A55B  call     0x20e600  ; -> 0020E600 fn
0045A560  mov      ecx, dword ptr [rbx + 0x14]
0045A563  lea      rdi, [rip + 0x2688a1e]  ; -> 02AE2F88
0045A56A  mov      r8d, dword ptr [rip + 0x2688a0b]  ; -> 02AE2F7C
0045A571  lea      r9, [rip + 0x50a48]  ; -> 004AAFC0
0045A578  mov      edx, dword ptr [rip + 0x26889fa]  ; -> 02AE2F78
0045A57E  mov      dword ptr [rsp + 0x38], ecx
0045A582  mov      ecx, esi
0045A584  mov      qword ptr [rsp + 0x30], rax
0045A589  mov      dword ptr [rsp + 0x28], 0x118
0045A591  mov      qword ptr [rsp + 0x20], rdi
0045A596  call     0x3a33b0  ; -> 003A33B0 fn
0045A59B  mov      dword ptr [rip + 0x26889eb], 0  ; -> 02AE2F90
0045A5A5  mov      ecx, dword ptr [rbx + 0x10]
0045A5A8  call     0x20e600  ; -> 0020E600 fn
0045A5AD  jmp      0x45a63f  ; -> 0045A63F
0045A5B2  mov      dword ptr [rip + 0x26889d4], 2  ; -> 02AE2F90
0045A5BC  jmp      0x45a5c8  ; -> 0045A5C8
0045A5BE  mov      dword ptr [rip + 0x26889c8], 0  ; -> 02AE2F90
0045A5C8  test     byte ptr [rdi + 0x25a], 7
0045A5CF  jne      0x45a60e  ; -> 0045A60E
0045A5D1  mov      ecx, dword ptr [rbx + 0x10]
0045A5D4  call     0x20e600  ; -> 0020E600 fn
0045A5D9  lea      r9, [rip + 0x26889a8]  ; -> 02AE2F88
0045A5E0  mov      ecx, dword ptr [rbx + 0x14]
0045A5E3  lea      r8, [rip + 0x509d6]  ; -> 004AAFC0
0045A5EA  mov      edx, dword ptr [rip + 0x268898c]  ; -> 02AE2F7C
0045A5F0  mov      dword ptr [rsp + 0x30], ecx
0045A5F4  mov      ecx, dword ptr [rip + 0x268897e]  ; -> 02AE2F78
0045A5FA  mov      qword ptr [rsp + 0x28], rax
0045A5FF  mov      dword ptr [rsp + 0x20], 0x118
0045A607  call     0x3a2f70  ; -> 003A2F70 fn
0045A60C  jmp      0x45a673  ; -> 0045A673
0045A60E  test     byte ptr [rdi + 0x4b], 1
0045A612  mov      rcx, rsi
0045A615  jne      0x45a629  ; -> 0045A629
0045A617  lea      rdx, [rbp - 0x59]
0045A61B  call     0x399600  ; -> 00399600 fn
0045A620  test     eax, eax
0045A622  jne      0x45a673  ; -> 0045A673
0045A624  mov      esi, dword ptr [rbp - 0x55]
0045A627  jmp      0x45a630  ; -> 0045A630
0045A629  call     0x39a9b0  ; -> 0039A9B0 fn
0045A62E  mov      esi, eax
0045A630  mov      ecx, dword ptr [rbx + 0x10]
0045A633  call     0x20e600  ; -> 0020E600 fn
0045A638  lea      rdi, [rip + 0x2688949]  ; -> 02AE2F88
0045A63F  mov      ecx, dword ptr [rbx + 0x14]
0045A642  lea      r9, [rip + 0x50977]  ; -> 004AAFC0
0045A649  mov      r8d, dword ptr [rip + 0x268892c]  ; -> 02AE2F7C
0045A650  mov      edx, dword ptr [rip + 0x2688922]  ; -> 02AE2F78
0045A656  mov      dword ptr [rsp + 0x38], ecx
0045A65A  mov      ecx, esi
0045A65C  mov      qword ptr [rsp + 0x30], rax
0045A661  mov      dword ptr [rsp + 0x28], 0x118
0045A669  mov      qword ptr [rsp + 0x20], rdi
0045A66E  call     0x3a33b0  ; -> 003A33B0 fn
0045A673  mov      rsi, qword ptr [rsp + 0x118]
0045A67B  mov      rdi, qword ptr [rsp + 0x120]
0045A683  mov      rcx, qword ptr [rbp + 0x47]
0045A687  xor      rcx, rsp
0045A68A  call     0x808c40  ; -> 00808C40 fn
0045A68F  mov      rbx, qword ptr [rsp + 0x128]
0045A697  add      rsp, 0x100
0045A69E  pop      rbp
0045A69F  ret      
```

## 0045A6A0 (937 B, extent 0045A6A0-0045AA49)

Page context: " stage.  Interior anchor '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call field step.  Interior anchor '003A2F94' (function '003A2F70"

```
0045A6A0  push     rbp
0045A6A2  push     rbx
0045A6A3  lea      rbp, [rsp - 8]
0045A6A8  sub      rsp, 0x108
0045A6AF  mov      rax, qword ptr [rip + 0x1aea17a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045A6B6  xor      rax, rsp
0045A6B9  mov      qword ptr [rbp - 0x10], rax
0045A6BD  cmp      byte ptr [rcx], 0
0045A6C0  mov      rbx, rcx
0045A6C3  je       0x45aa33  ; -> 0045AA33
0045A6C9  movups   xmm0, xmmword ptr [rcx + 0x250]
0045A6D0  mov      qword ptr [rsp + 0x130], rdi
0045A6D8  movups   xmm1, xmmword ptr [rcx + 0x260]
0045A6DF  mov      rdi, qword ptr [rcx + 0x20]
0045A6E3  movups   xmmword ptr [rsp + 0x60], xmm0
0045A6E8  movups   xmm0, xmmword ptr [rcx + 0x270]
0045A6EF  movups   xmmword ptr [rsp + 0x70], xmm1
0045A6F4  movups   xmm1, xmmword ptr [rcx + 0x280]
0045A6FB  movups   xmmword ptr [rbp - 0x80], xmm0
0045A6FF  movups   xmmword ptr [rbp - 0x70], xmm1
0045A703  movzx    ecx, byte ptr [rdi + 0x4a]
0045A707  shr      ecx, 2
0045A70A  and      ecx, 7
0045A70D  sub      ecx, 1
0045A710  je       0x45a750  ; -> 0045A750
0045A712  sub      ecx, 1
0045A715  je       0x45a747  ; -> 0045A747
0045A717  sub      ecx, 2
0045A71A  je       0x45a734  ; -> 0045A734
0045A71C  cmp      ecx, 1
0045A71F  jne      0x45a761  ; -> 0045A761
0045A721  lea      rcx, [rsp + 0x60]
0045A726  call     0x434a70  ; -> 00434A70 fn
0045A72B  lea      rcx, [rip + 0x269432e]  ; -> 02AEEA60
0045A732  jmp      0x45a757  ; -> 0045A757
0045A734  lea      rcx, [rsp + 0x60]
0045A739  call     0x434900  ; -> 00434900 fn
0045A73E  lea      rcx, [rip + 0x269431b]  ; -> 02AEEA60
0045A745  jmp      0x45a757  ; -> 0045A757
0045A747  lea      rcx, [rip + 0x2694522]  ; -> 02AEEC70
0045A74E  jmp      0x45a757  ; -> 0045A757
0045A750  lea      rcx, [rip + 0x26944d9]  ; -> 02AEEC30
0045A757  lea      rdx, [rsp + 0x60]
0045A75C  call     0x398030  ; -> 00398030 fn
0045A761  mov      ecx, dword ptr [rbx + 0x290]
0045A767  call     0x39b620  ; -> 0039B620 fn
0045A76C  lea      rcx, [rip + 0x269453d]  ; -> 02AEECB0
0045A773  call     0x39b550  ; -> 0039B550 fn
0045A778  lea      rcx, [rbp - 0x50]
0045A77C  call     0x3970a0  ; -> 003970A0 fn
0045A781  lea      r8, [rip + 0x26879a8]  ; -> 02AE2130
0045A788  lea      rdx, [rsp + 0x60]
0045A78D  lea      rcx, [rbp - 0x50]
0045A791  call     0x397910  ; -> 00397910 fn
0045A796  movzx    eax, byte ptr [rdi + 0x250]
0045A79D  sub      al, 2
0045A79F  test     al, 0xfd
0045A7A1  jne      0x45aa2b  ; -> 0045AA2B
0045A7A7  mov      r9d, dword ptr [rbx + 0x44]
0045A7AB  lea      rdx, [rsp + 0x50]
0045A7B0  xor      r8d, r8d
0045A7B3  mov      qword ptr [rsp + 0x128], rsi
0045A7BB  lea      rcx, [rdi + 0x1b0]
0045A7C2  call     0x431830  ; -> 00431830 fn
0045A7C7  test     rax, rax
0045A7CA  je       0x45aa23  ; -> 0045AA23
0045A7D0  mov      edx, dword ptr [rbx + 0x44]
0045A7D3  lea      rcx, [rdi + 0x30]
0045A7D7  mov      qword ptr [rsp + 0x100], r14
0045A7DF  call     0x4314e0  ; -> 004314E0 fn
0045A7E4  movsxd   rdx, eax
0045A7E7  lea      rcx, [rdi + 0x1b0]
0045A7EE  movzx    eax, word ptr [rdi + 0x25a]
0045A7F5  and      eax, 7
0045A7F8  mov      qword ptr [rip + 0x2694109], rdx  ; -> 02AEE908
0045A7FF  mov      dword ptr [rip + 0x26940fb], eax  ; -> 02AEE900
0045A805  mov      rax, qword ptr [rsp + 0x58]
0045A80A  mov      qword ptr [rip + 0x268796f], rax  ; -> 02AE2180
0045A811  mov      rax, qword ptr [rsp + 0x50]
0045A816  mov      qword ptr [rip + 0x2687973], rax  ; -> 02AE2190
0045A81D  mov      edx, dword ptr [rbx + 0x44]
0045A820  call     0x4309c0  ; -> 004309C0 fn
0045A825  movss    dword ptr [rip + 0x26878a3], xmm0  ; -> 02AE20D0
0045A82D  lea      rcx, [rdi + 0x1c0]
0045A834  mov      edx, dword ptr [rbx + 0x44]
0045A837  call     0x4309c0  ; -> 004309C0 fn
0045A83C  movss    xmm1, dword ptr [rip + 0x268788c]  ; -> 02AE20D0
0045A844  lea      r14, [rbx + 0x230]
0045A84B  movss    dword ptr [rip + 0x2687881], xmm0  ; -> 02AE20D4
0045A853  lea      r8, [rsp + 0x44]
0045A858  addss    xmm1, dword ptr [rbx + 0x29c]
0045A860  mov      rdx, r14
0045A863  mov      rcx, rbx
0045A866  movss    dword ptr [rip + 0x2687862], xmm1  ; -> 02AE20D0
0045A86E  addss    xmm0, dword ptr [rbx + 0x2a0]
0045A876  movss    dword ptr [rip + 0x2687856], xmm0  ; -> 02AE20D4
0045A87E  call     0x2f1f40  ; -> 002F1F40 fn
0045A883  lea      rdx, [rbx + 0x240]
0045A88A  lea      r8, [rsp + 0x44]
0045A88F  lea      rcx, [rsp + 0x44]
0045A894  call     0x26ee00  ; -> 0026EE00 fn
0045A899  mov      edx, dword ptr [rbx + 0x44]
0045A89C  lea      rcx, [rdi + 0x1f0]
0045A8A3  call     0x42fdb0  ; -> 0042FDB0 fn
0045A8A8  lea      r8, [rsp + 0x44]
0045A8AD  mov      dword ptr [rsp + 0x40], eax
0045A8B1  lea      rdx, [rsp + 0x40]
0045A8B6  lea      rcx, [rsp + 0x40]
0045A8BB  call     0x26ee00  ; -> 0026EE00 fn
0045A8C0  movzx    eax, byte ptr [rsp + 0x40]
0045A8C5  lea      rcx, [rdi + 0x190]
0045A8CC  mov      dword ptr [rip + 0x26877ee], eax  ; -> 02AE20C0
0045A8D2  movzx    eax, byte ptr [rsp + 0x41]
0045A8D7  mov      dword ptr [rip + 0x26877e7], eax  ; -> 02AE20C4
0045A8DD  movzx    eax, byte ptr [rsp + 0x42]
0045A8E2  mov      dword ptr [rip + 0x26877e0], eax  ; -> 02AE20C8
0045A8E8  movzx    eax, byte ptr [rsp + 0x43]
0045A8ED  mov      dword ptr [rip + 0x26877d9], eax  ; -> 02AE20CC
0045A8F3  mov      edx, dword ptr [rbx + 0x44]
0045A8F6  call     0x4309c0  ; -> 004309C0 fn
0045A8FB  movss    dword ptr [rip + 0x26877d9], xmm0  ; -> 02AE20DC
0045A903  test     byte ptr [rdi + 0x2a4], 1
0045A90A  je       0x45a921  ; -> 0045A921
0045A90C  movsxd   rax, dword ptr [rbx + 0x298]
0045A913  mov      ecx, dword ptr [rdi + rax*4 + 0x2b0]
0045A91A  call     0x20e600  ; -> 0020E600 fn
0045A91F  jmp      0x45a958  ; -> 0045A958
0045A921  cvttss2si esi, xmm0
0045A925  cmp      esi, 3
0045A928  ja       0x45aa1b  ; -> 0045AA1B
0045A92E  movsxd   rax, esi
0045A931  mov      ecx, dword ptr [rdi + rax*4 + 0x2b0]
0045A938  call     0x20e600  ; -> 0020E600 fn
0045A93D  movss    xmm1, dword ptr [rip + 0x2687797]  ; -> 02AE20DC
0045A945  movd     xmm0, esi
0045A949  cvtdq2ps xmm0, xmm0
0045A94C  subss    xmm1, xmm0
0045A950  movss    dword ptr [rip + 0x2687784], xmm1  ; -> 02AE20DC
0045A958  mov      rbx, rax
0045A95B  test     rax, rax
0045A95E  je       0x45aa1b  ; -> 0045AA1B
0045A964  test     byte ptr [rdi + 0x25a], 7
0045A96B  jne      0x45a9aa  ; -> 0045A9AA
0045A96D  mov      ecx, dword ptr [rax + 0x10]
0045A970  call     0x20e600  ; -> 0020E600 fn
0045A975  mov      ecx, dword ptr [rbx + 0x14]
0045A978  lea      r9, [rip + 0x2687719]  ; -> 02AE2098
0045A97F  mov      edx, dword ptr [rip + 0x2687707]  ; -> 02AE208C
0045A985  lea      r8, [rip + 0x4e174]  ; -> 004A8B00
0045A98C  mov      dword ptr [rsp + 0x30], ecx
0045A990  mov      ecx, dword ptr [rip + 0x26876f2]  ; -> 02AE2088
0045A996  mov      qword ptr [rsp + 0x28], rax
0045A99B  mov      dword ptr [rsp + 0x20], 0x118
0045A9A3  call     0x3a2f70  ; -> 003A2F70 fn
0045A9A8  jmp      0x45aa1b  ; -> 0045AA1B
0045A9AA  lea      rcx, [rip + 0x26942ff]  ; -> 02AEECB0
0045A9B1  call     0x39b550  ; -> 0039B550 fn
0045A9B6  test     byte ptr [rdi + 0x4b], 1
0045A9BA  mov      rcx, r14
0045A9BD  jne      0x45a9d1  ; -> 0045A9D1
0045A9BF  lea      rdx, [rbp - 0x60]
0045A9C3  call     0x399600  ; -> 00399600 fn
0045A9C8  test     eax, eax
0045A9CA  jne      0x45aa1b  ; -> 0045AA1B
0045A9CC  mov      edi, dword ptr [rbp - 0x5c]
0045A9CF  jmp      0x45a9d8  ; -> 0045A9D8
0045A9D1  call     0x39a9b0  ; -> 0039A9B0 fn
0045A9D6  mov      edi, eax
0045A9D8  mov      ecx, dword ptr [rbx + 0x10]
0045A9DB  call     0x20e600  ; -> 0020E600 fn
0045A9E0  mov      ecx, dword ptr [rbx + 0x14]
0045A9E3  lea      r9, [rip + 0x4e116]  ; -> 004A8B00
0045A9EA  mov      r8d, dword ptr [rip + 0x268769b]  ; -> 02AE208C
0045A9F1  mov      edx, dword ptr [rip + 0x2687691]  ; -> 02AE2088
0045A9F7  mov      dword ptr [rsp + 0x38], ecx
0045A9FB  mov      ecx, edi
0045A9FD  mov      qword ptr [rsp + 0x30], rax
0045AA02  lea      rax, [rip + 0x268768f]  ; -> 02AE2098
0045AA09  mov      dword ptr [rsp + 0x28], 0x118
0045AA11  mov      qword ptr [rsp + 0x20], rax
0045AA16  call     0x3a33b0  ; -> 003A33B0 fn
0045AA1B  mov      r14, qword ptr [rsp + 0x100]
0045AA23  mov      rsi, qword ptr [rsp + 0x128]
0045AA2B  mov      rdi, qword ptr [rsp + 0x130]
0045AA33  mov      rcx, qword ptr [rbp - 0x10]
0045AA37  xor      rcx, rsp
0045AA3A  call     0x808c40  ; -> 00808C40 fn
0045AA3F  add      rsp, 0x108
0045AA46  pop      rbx
0045AA47  pop      rbp
0045AA48  ret      
```

## 0045AEF0 (867 B, extent 0045AEF0-0045B253)

Page context: "erior anchor '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call field step.  Interior anchor '003A2F94' (function '003A2F70').  '004509"

```
0045AEF0  push     rbp
0045AEF2  push     rbx
0045AEF3  push     rdi
0045AEF4  lea      rbp, [rsp - 0x47]
0045AEF9  sub      rsp, 0x100
0045AF00  mov      rax, qword ptr [rip + 0x1ae9929]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045AF07  xor      rax, rsp
0045AF0A  mov      qword ptr [rbp + 0x37], rax
0045AF0E  movups   xmm0, xmmword ptr [rcx + 0x250]
0045AF15  mov      rdi, qword ptr [rcx + 0x20]
0045AF19  mov      rbx, rcx
0045AF1C  movups   xmm1, xmmword ptr [rcx + 0x260]
0045AF23  movups   xmmword ptr [rbp - 0x69], xmm0
0045AF27  movups   xmm0, xmmword ptr [rcx + 0x270]
0045AF2E  movups   xmmword ptr [rbp - 0x59], xmm1
0045AF32  movups   xmm1, xmmword ptr [rcx + 0x280]
0045AF39  movups   xmmword ptr [rbp - 0x49], xmm0
0045AF3D  movups   xmmword ptr [rbp - 0x39], xmm1
0045AF41  movzx    ecx, byte ptr [rdi + 0x4a]
0045AF45  shr      ecx, 2
0045AF48  and      ecx, 7
0045AF4B  sub      ecx, 1
0045AF4E  je       0x45af8c  ; -> 0045AF8C
0045AF50  sub      ecx, 1
0045AF53  je       0x45af83  ; -> 0045AF83
0045AF55  sub      ecx, 2
0045AF58  je       0x45af71  ; -> 0045AF71
0045AF5A  cmp      ecx, 1
0045AF5D  jne      0x45af9c  ; -> 0045AF9C
0045AF5F  lea      rcx, [rbp - 0x69]
0045AF63  call     0x434a70  ; -> 00434A70 fn
0045AF68  lea      rcx, [rip + 0x2693af1]  ; -> 02AEEA60
0045AF6F  jmp      0x45af93  ; -> 0045AF93
0045AF71  lea      rcx, [rbp - 0x69]
0045AF75  call     0x434900  ; -> 00434900 fn
0045AF7A  lea      rcx, [rip + 0x2693adf]  ; -> 02AEEA60
0045AF81  jmp      0x45af93  ; -> 0045AF93
0045AF83  lea      rcx, [rip + 0x2693ce6]  ; -> 02AEEC70
0045AF8A  jmp      0x45af93  ; -> 0045AF93
0045AF8C  lea      rcx, [rip + 0x2693c9d]  ; -> 02AEEC30
0045AF93  lea      rdx, [rbp - 0x69]
0045AF97  call     0x398030  ; -> 00398030 fn
0045AF9C  mov      ecx, dword ptr [rbx + 0x290]
0045AFA2  call     0x39b620  ; -> 0039B620 fn
0045AFA7  lea      rcx, [rip + 0x2693d02]  ; -> 02AEECB0
0045AFAE  call     0x39b550  ; -> 0039B550 fn
0045AFB3  lea      rcx, [rbp - 9]
0045AFB7  call     0x3970a0  ; -> 003970A0 fn
0045AFBC  lea      r8, [rip + 0x26882dd]  ; -> 02AE32A0
0045AFC3  lea      rdx, [rbp - 0x69]
0045AFC7  lea      rcx, [rbp - 9]
0045AFCB  call     0x397910  ; -> 00397910 fn
0045AFD0  lea      r8, [rbp - 0x69]
0045AFD4  lea      rdx, [rbp - 0x69]
0045AFD8  lea      rcx, [rip + 0x2693a41]  ; -> 02AEEA20
0045AFDF  call     0x397910  ; -> 00397910 fn
0045AFE4  lea      r8, [rip + 0x2688265]  ; -> 02AE3250
0045AFEB  lea      rdx, [rbp - 0x69]
0045AFEF  lea      rcx, [rip + 0x2692dfa]  ; -> 02AEDDF0
0045AFF6  call     0x397910  ; -> 00397910 fn
0045AFFB  movzx    eax, byte ptr [rdi + 0x240]
0045B002  sub      al, 2
0045B004  test     al, 0xfd
0045B006  jne      0x45b23c  ; -> 0045B23C
0045B00C  mov      r9d, dword ptr [rbx + 0x44]
0045B010  lea      rdx, [rbp - 0x29]
0045B014  xor      r8d, r8d
0045B017  mov      qword ptr [rsp + 0x128], rsi
0045B01F  lea      rcx, [rdi + 0x1a0]
0045B026  call     0x431830  ; -> 00431830 fn
0045B02B  test     rax, rax
0045B02E  je       0x45b234  ; -> 0045B234
0045B034  mov      edx, dword ptr [rbx + 0x44]
0045B037  lea      rcx, [rdi + 0x30]
0045B03B  mov      qword ptr [rsp + 0x130], r14
0045B043  call     0x4314e0  ; -> 004314E0 fn
0045B048  movsxd   rdx, eax
0045B04B  lea      rcx, [rdi + 0x1a0]
0045B052  movzx    eax, word ptr [rdi + 0x24a]
0045B059  and      eax, 7
0045B05C  mov      qword ptr [rip + 0x26938a5], rdx  ; -> 02AEE908
0045B063  mov      dword ptr [rip + 0x2693897], eax  ; -> 02AEE900
0045B069  mov      rax, qword ptr [rbp - 0x29]
0045B06D  mov      qword ptr [rip + 0x268828c], rax  ; -> 02AE3300
0045B074  mov      rax, qword ptr [rbp - 0x21]
0045B078  mov      qword ptr [rip + 0x2688271], rax  ; -> 02AE32F0
0045B07F  mov      edx, dword ptr [rbx + 0x44]
0045B082  call     0x4309c0  ; -> 004309C0 fn
0045B087  movss    dword ptr [rip + 0x26881b1], xmm0  ; -> 02AE3240
0045B08F  lea      rcx, [rdi + 0x1b0]
0045B096  mov      edx, dword ptr [rbx + 0x44]
0045B099  call     0x4309c0  ; -> 004309C0 fn
0045B09E  movss    xmm1, dword ptr [rip + 0x268819a]  ; -> 02AE3240
0045B0A6  lea      r8, [rbp - 0x75]
0045B0AA  movss    dword ptr [rip + 0x2688192], xmm0  ; -> 02AE3244
0045B0B2  lea      rdx, [rbx + 0x230]
0045B0B9  addss    xmm1, dword ptr [rbx + 0x29c]
0045B0C1  mov      rcx, rbx
0045B0C4  movss    dword ptr [rip + 0x2688174], xmm1  ; -> 02AE3240
0045B0CC  addss    xmm0, dword ptr [rbx + 0x2a0]
0045B0D4  movss    dword ptr [rip + 0x2688168], xmm0  ; -> 02AE3244
0045B0DC  call     0x2f1f40  ; -> 002F1F40 fn
0045B0E1  lea      rdx, [rbx + 0x240]
0045B0E8  lea      r8, [rbp - 0x75]
0045B0EC  lea      rcx, [rbp - 0x75]
0045B0F0  call     0x26ee00  ; -> 0026EE00 fn
0045B0F5  mov      edx, dword ptr [rbx + 0x44]
0045B0F8  lea      rcx, [rdi + 0x1e0]
0045B0FF  call     0x42fdb0  ; -> 0042FDB0 fn
0045B104  lea      r8, [rbp - 0x75]
0045B108  mov      dword ptr [rbp - 0x79], eax
0045B10B  lea      rdx, [rbp - 0x79]
0045B10F  lea      rcx, [rbp - 0x79]
0045B113  call     0x26ee00  ; -> 0026EE00 fn
0045B118  movzx    eax, byte ptr [rbp - 0x79]
0045B11C  mov      dword ptr [rip + 0x268810e], eax  ; -> 02AE3230
0045B122  movzx    eax, byte ptr [rbp - 0x78]
0045B126  mov      dword ptr [rip + 0x2688108], eax  ; -> 02AE3234
0045B12C  movzx    eax, byte ptr [rbp - 0x77]
0045B130  mov      dword ptr [rip + 0x2688102], eax  ; -> 02AE3238
0045B136  movzx    eax, byte ptr [rbp - 0x76]
0045B13A  mov      dword ptr [rip + 0x26880fc], eax  ; -> 02AE323C
0045B140  movsxd   rax, dword ptr [rbx + 0x298]
0045B147  mov      ecx, dword ptr [rdi + rax*4 + 0x2a0]
0045B14E  call     0x20e600  ; -> 0020E600 fn
0045B153  mov      rsi, rax
0045B156  test     rax, rax
0045B159  je       0x45b22c  ; -> 0045B22C
0045B15F  test     byte ptr [rdi + 0x24a], 7
0045B166  jne      0x45b1a8  ; -> 0045B1A8
0045B168  mov      ecx, dword ptr [rax + 0x10]
0045B16B  call     0x20e600  ; -> 0020E600 fn
0045B170  mov      ecx, dword ptr [rsi + 0x14]
0045B173  lea      r9, [rip + 0x268808e]  ; -> 02AE3208
0045B17A  mov      edx, dword ptr [rip + 0x268807c]  ; -> 02AE31FC
0045B180  lea      r8, [rip + 0x52b89]  ; -> 004ADD10
0045B187  mov      dword ptr [rsp + 0x30], ecx
0045B18B  mov      ecx, dword ptr [rip + 0x2688067]  ; -> 02AE31F8
0045B191  mov      qword ptr [rsp + 0x28], rax
0045B196  mov      dword ptr [rsp + 0x20], 0x128
0045B19E  call     0x3a2f70  ; -> 003A2F70 fn
0045B1A3  jmp      0x45b22c  ; -> 0045B22C
0045B1A8  lea      rcx, [rip + 0x2693b01]  ; -> 02AEECB0
0045B1AF  call     0x39b550  ; -> 0039B550 fn
0045B1B4  test     byte ptr [rdi + 0x4b], 1
0045B1B8  lea      rcx, [rbx + 0x230]
0045B1BF  jne      0x45b1e2  ; -> 0045B1E2
0045B1C1  lea      rdx, [rbp - 0x19]
0045B1C5  call     0x399600  ; -> 00399600 fn
0045B1CA  test     eax, eax
0045B1CC  jne      0x45b22c  ; -> 0045B22C
0045B1CE  mov      ecx, dword ptr [rsi + 0x10]
0045B1D1  call     0x20e600  ; -> 0020E600 fn
0045B1D6  mov      ecx, dword ptr [rsi + 0x14]
0045B1D9  mov      dword ptr [rsp + 0x38], ecx
0045B1DD  mov      ecx, dword ptr [rbp - 0x15]
0045B1E0  jmp      0x45b1fa  ; -> 0045B1FA
0045B1E2  call     0x39a9b0  ; -> 0039A9B0 fn
0045B1E7  mov      ecx, dword ptr [rsi + 0x10]
0045B1EA  mov      ebx, eax
0045B1EC  call     0x20e600  ; -> 0020E600 fn
0045B1F1  mov      ecx, dword ptr [rsi + 0x14]
0045B1F4  mov      dword ptr [rsp + 0x38], ecx
0045B1F8  mov      ecx, ebx
0045B1FA  mov      r8d, dword ptr [rip + 0x2687ffb]  ; -> 02AE31FC
0045B201  lea      r9, [rip + 0x52b08]  ; -> 004ADD10
0045B208  mov      edx, dword ptr [rip + 0x2687fea]  ; -> 02AE31F8
0045B20E  mov      qword ptr [rsp + 0x30], rax
0045B213  lea      rax, [rip + 0x2687fee]  ; -> 02AE3208
0045B21A  mov      dword ptr [rsp + 0x28], 0x128
0045B222  mov      qword ptr [rsp + 0x20], rax
0045B227  call     0x3a33b0  ; -> 003A33B0 fn
0045B22C  mov      r14, qword ptr [rsp + 0x130]
0045B234  mov      rsi, qword ptr [rsp + 0x128]
0045B23C  mov      rcx, qword ptr [rbp + 0x37]
0045B240  xor      rcx, rsp
0045B243  call     0x808c40  ; -> 00808C40 fn
0045B248  add      rsp, 0x100
0045B24F  pop      rdi
0045B250  pop      rbx
0045B251  pop      rbp
0045B252  ret      
```

## 0045B2B0 (902 B, extent 0045B2B0-0045B636)

Page context: " '0044E41D' (function '0044E160').  '003A2F70' (154 B) is the shared mid-ladder helper eight '0045xxxx' type arms ('00455560', '004559C0', '00455DB0', '00456720', '0045A220', '0045A6A0', '0045AEF0', '0045B2B0') call: 'ecx'/'edx'/'r8'/'r9' args are marshalled onto the stack for '0020E680', then '001DB840' runs the second stage - the element arms' two-call field step.  Interior anchor '003A2F94' (function '003A2F70').  '00450940' (918 B) "

```
0045B2B0  push     rbp
0045B2B2  push     rbx
0045B2B3  push     rdi
0045B2B4  lea      rbp, [rsp - 0x10]
0045B2B9  sub      rsp, 0x110
0045B2C0  mov      rax, qword ptr [rip + 0x1ae9569]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045B2C7  xor      rax, rsp
0045B2CA  mov      qword ptr [rbp - 0x10], rax
0045B2CE  movups   xmm0, xmmword ptr [rcx + 0x250]
0045B2D5  mov      rdi, qword ptr [rcx + 0x20]
0045B2D9  mov      rbx, rcx
0045B2DC  movups   xmm1, xmmword ptr [rcx + 0x260]
0045B2E3  movups   xmmword ptr [rsp + 0x60], xmm0
0045B2E8  movups   xmm0, xmmword ptr [rcx + 0x270]
0045B2EF  movups   xmmword ptr [rsp + 0x70], xmm1
0045B2F4  movups   xmm1, xmmword ptr [rcx + 0x280]
0045B2FB  movups   xmmword ptr [rbp - 0x80], xmm0
0045B2FF  movups   xmmword ptr [rbp - 0x70], xmm1
0045B303  movzx    ecx, byte ptr [rdi + 0x4a]
0045B307  shr      ecx, 2
0045B30A  and      ecx, 7
0045B30D  sub      ecx, 1
0045B310  je       0x45b350  ; -> 0045B350
0045B312  sub      ecx, 1
0045B315  je       0x45b347  ; -> 0045B347
0045B317  sub      ecx, 2
0045B31A  je       0x45b334  ; -> 0045B334
0045B31C  cmp      ecx, 1
0045B31F  jne      0x45b361  ; -> 0045B361
0045B321  lea      rcx, [rsp + 0x60]
0045B326  call     0x434a70  ; -> 00434A70 fn
0045B32B  lea      rcx, [rip + 0x269372e]  ; -> 02AEEA60
0045B332  jmp      0x45b357  ; -> 0045B357
0045B334  lea      rcx, [rsp + 0x60]
0045B339  call     0x434900  ; -> 00434900 fn
0045B33E  lea      rcx, [rip + 0x269371b]  ; -> 02AEEA60
0045B345  jmp      0x45b357  ; -> 0045B357
0045B347  lea      rcx, [rip + 0x2693922]  ; -> 02AEEC70
0045B34E  jmp      0x45b357  ; -> 0045B357
0045B350  lea      rcx, [rip + 0x26938d9]  ; -> 02AEEC30
0045B357  lea      rdx, [rsp + 0x60]
0045B35C  call     0x398030  ; -> 00398030 fn
0045B361  lea      r8, [rbp - 0x60]
0045B365  lea      rdx, [rsp + 0x60]
0045B36A  lea      rcx, [rip + 0x269387f]  ; -> 02AEEBF0
0045B371  call     0x397910  ; -> 00397910 fn
0045B376  lea      rdx, [rbp - 0x60]
0045B37A  lea      rcx, [rbp - 0x60]
0045B37E  call     0x39b960  ; -> 0039B960 fn
0045B383  lea      rdx, [rbp - 0x50]
0045B387  lea      rcx, [rbp - 0x50]
0045B38B  call     0x39b960  ; -> 0039B960 fn
0045B390  lea      rdx, [rbp - 0x40]
0045B394  lea      rcx, [rbp - 0x40]
0045B398  call     0x39b960  ; -> 0039B960 fn
0045B39D  movaps   xmm0, xmmword ptr [rbp - 0x60]
0045B3A1  movaps   xmm1, xmmword ptr [rbp - 0x50]
0045B3A5  movups   xmmword ptr [rip + 0x2687ff4], xmm0  ; -> 02AE33A0
0045B3AC  movaps   xmm0, xmmword ptr [rbp - 0x40]
0045B3B0  movups   xmmword ptr [rip + 0x2688009], xmm0  ; -> 02AE33C0
0045B3B7  movups   xmmword ptr [rip + 0x2687ff2], xmm1  ; -> 02AE33B0
0045B3BE  mov      ecx, dword ptr [rbx + 0x290]
0045B3C4  call     0x39b620  ; -> 0039B620 fn
0045B3C9  lea      rcx, [rip + 0x26938e0]  ; -> 02AEECB0
0045B3D0  call     0x39b550  ; -> 0039B550 fn
0045B3D5  lea      rcx, [rbp - 0x60]
0045B3D9  call     0x3970a0  ; -> 003970A0 fn
0045B3DE  lea      r8, [rip + 0x2687ffb]  ; -> 02AE33E0
0045B3E5  lea      rdx, [rsp + 0x60]
0045B3EA  lea      rcx, [rbp - 0x60]
0045B3EE  call     0x397910  ; -> 00397910 fn
0045B3F3  movzx    eax, byte ptr [rdi + 0x240]
0045B3FA  sub      al, 2
0045B3FC  test     al, 0xfd
0045B3FE  jne      0x45b61f  ; -> 0045B61F
0045B404  mov      r9d, dword ptr [rbx + 0x44]
0045B408  lea      rcx, [rdi + 0x1a0]
0045B40F  xor      r8d, r8d
0045B412  lea      rdx, [rsp + 0x50]
0045B417  call     0x431830  ; -> 00431830 fn
0045B41C  test     rax, rax
0045B41F  je       0x45b61f  ; -> 0045B61F
0045B425  mov      edx, dword ptr [rbx + 0x44]
0045B428  lea      rcx, [rdi + 0x30]
0045B42C  mov      qword ptr [rsp + 0x138], rsi
0045B434  mov      qword ptr [rsp + 0x140], r14
0045B43C  movaps   xmmword ptr [rsp + 0x100], xmm6
0045B444  call     0x4314e0  ; -> 004314E0 fn
0045B449  movsxd   rcx, eax
0045B44C  movzx    eax, word ptr [rdi + 0x24a]
0045B453  and      eax, 7
0045B456  mov      qword ptr [rip + 0x26934ab], rcx  ; -> 02AEE908
0045B45D  mov      dword ptr [rip + 0x269349d], eax  ; -> 02AEE900
0045B463  lea      rcx, [rdi + 0x230]
0045B46A  mov      rax, qword ptr [rsp + 0x50]
0045B46F  mov      qword ptr [rip + 0x2687fca], rax  ; -> 02AE3440
0045B476  mov      rax, qword ptr [rsp + 0x58]
0045B47B  mov      qword ptr [rip + 0x2687fae], rax  ; -> 02AE3430
0045B482  mov      edx, dword ptr [rbx + 0x44]
0045B485  call     0x4309c0  ; -> 004309C0 fn
0045B48A  movaps   xmm6, xmm0
0045B48D  call     0x17ffd0  ; -> 0017FFD0 fn
0045B492  mulss    xmm6, xmm0
0045B496  lea      r8, [rsp + 0x44]
0045B49B  lea      rdx, [rbx + 0x230]
0045B4A2  mov      rcx, rbx
0045B4A5  movss    dword ptr [rip + 0x2687edf], xmm6  ; -> 02AE338C
0045B4AD  call     0x2f1f40  ; -> 002F1F40 fn
0045B4B2  lea      rdx, [rbx + 0x240]
0045B4B9  lea      r8, [rsp + 0x44]
0045B4BE  lea      rcx, [rsp + 0x44]
0045B4C3  call     0x26ee00  ; -> 0026EE00 fn
0045B4C8  mov      edx, dword ptr [rbx + 0x44]
0045B4CB  lea      rcx, [rdi + 0x1e0]
0045B4D2  call     0x42fdb0  ; -> 0042FDB0 fn
0045B4D7  lea      r8, [rsp + 0x44]
0045B4DC  mov      dword ptr [rsp + 0x40], eax
0045B4E0  lea      rdx, [rsp + 0x40]
0045B4E5  lea      rcx, [rsp + 0x40]
0045B4EA  call     0x26ee00  ; -> 0026EE00 fn
0045B4EF  movzx    eax, byte ptr [rsp + 0x40]
0045B4F4  mov      dword ptr [rip + 0x2687e76], eax  ; -> 02AE3370
0045B4FA  movzx    eax, byte ptr [rsp + 0x41]
0045B4FF  mov      dword ptr [rip + 0x2687e6f], eax  ; -> 02AE3374
0045B505  movzx    eax, byte ptr [rsp + 0x42]
0045B50A  mov      dword ptr [rip + 0x2687e68], eax  ; -> 02AE3378
0045B510  movzx    eax, byte ptr [rsp + 0x43]
0045B515  mov      dword ptr [rip + 0x2687e61], eax  ; -> 02AE337C
0045B51B  movsxd   rax, dword ptr [rbx + 0x298]
0045B522  mov      ecx, dword ptr [rdi + rax*4 + 0x2a0]
0045B529  call     0x20e600  ; -> 0020E600 fn
0045B52E  movaps   xmm6, xmmword ptr [rsp + 0x100]
0045B536  mov      rsi, rax
0045B539  test     rax, rax
0045B53C  je       0x45b60f  ; -> 0045B60F
0045B542  test     byte ptr [rdi + 0x24a], 7
0045B549  jne      0x45b58b  ; -> 0045B58B
0045B54B  mov      ecx, dword ptr [rax + 0x10]
0045B54E  call     0x20e600  ; -> 0020E600 fn
0045B553  mov      ecx, dword ptr [rsi + 0x14]
0045B556  lea      r9, [rip + 0x2687deb]  ; -> 02AE3348
0045B55D  mov      edx, dword ptr [rip + 0x2687dd9]  ; -> 02AE333C
0045B563  lea      r8, [rip + 0x54cc6]  ; -> 004B0230
0045B56A  mov      dword ptr [rsp + 0x30], ecx
0045B56E  mov      ecx, dword ptr [rip + 0x2687dc4]  ; -> 02AE3338
0045B574  mov      qword ptr [rsp + 0x28], rax
0045B579  mov      dword ptr [rsp + 0x20], 0x118
0045B581  call     0x3a2f70  ; -> 003A2F70 fn
0045B586  jmp      0x45b60f  ; -> 0045B60F
0045B58B  lea      rcx, [rip + 0x269371e]  ; -> 02AEECB0
0045B592  call     0x39b550  ; -> 0039B550 fn
0045B597  test     byte ptr [rdi + 0x4b], 1
0045B59B  lea      rcx, [rbx + 0x230]
0045B5A2  jne      0x45b5c5  ; -> 0045B5C5
0045B5A4  lea      rdx, [rbp - 0x20]
0045B5A8  call     0x399600  ; -> 00399600 fn
0045B5AD  test     eax, eax
0045B5AF  jne      0x45b60f  ; -> 0045B60F
0045B5B1  mov      ecx, dword ptr [rsi + 0x10]
0045B5B4  call     0x20e600  ; -> 0020E600 fn
0045B5B9  mov      ecx, dword ptr [rsi + 0x14]
0045B5BC  mov      dword ptr [rsp + 0x38], ecx
0045B5C0  mov      ecx, dword ptr [rbp - 0x1c]
0045B5C3  jmp      0x45b5dd  ; -> 0045B5DD
0045B5C5  call     0x39a9b0  ; -> 0039A9B0 fn
0045B5CA  mov      ecx, dword ptr [rsi + 0x10]
0045B5CD  mov      ebx, eax
0045B5CF  call     0x20e600  ; -> 0020E600 fn
0045B5D4  mov      ecx, dword ptr [rsi + 0x14]
0045B5D7  mov      dword ptr [rsp + 0x38], ecx
0045B5DB  mov      ecx, ebx
0045B5DD  mov      r8d, dword ptr [rip + 0x2687d58]  ; -> 02AE333C
0045B5E4  lea      r9, [rip + 0x54c45]  ; -> 004B0230
0045B5EB  mov      edx, dword ptr [rip + 0x2687d47]  ; -> 02AE3338
0045B5F1  mov      qword ptr [rsp + 0x30], rax
0045B5F6  lea      rax, [rip + 0x2687d4b]  ; -> 02AE3348
0045B5FD  mov      dword ptr [rsp + 0x28], 0x118
0045B605  mov      qword ptr [rsp + 0x20], rax
0045B60A  call     0x3a33b0  ; -> 003A33B0 fn
0045B60F  mov      rsi, qword ptr [rsp + 0x138]
0045B617  mov      r14, qword ptr [rsp + 0x140]
0045B61F  mov      rcx, qword ptr [rbp - 0x10]
0045B623  xor      rcx, rsp
0045B626  call     0x808c40  ; -> 00808C40 fn
0045B62B  add      rsp, 0x110
0045B632  pop      rdi
0045B633  pop      rbx
0045B634  pop      rbp
0045B635  ret      
```

## 00463FF0 (81 B, extent 00463FF0-00464041)

Page context: "F0' packs the record to '[rbx+0x230]', '00377190' a second index to '[rbx+0x234]', '003D8D70' closes.  Interior anchor '0047BE49' (function '0047BE20').  '00377190' (148 B) is the handle-slot issuer '00463FF0'/'00464B30'/'00464F20'/'0047BE20' call on the '02ADBFE0' table (128 entries x 0x20, '[rax]' zero = free): serial '02ADBFC4' increments (wraps at 0xFFFFFF), packs '(serial<<8)|slot' into '[rax]', stores the caller's pointer at '+8',"

```
00463FF0  push     rbx
00463FF2  sub      rsp, 0x20
00463FF6  mov      rbx, rcx
00463FF9  call     0x2f2d60  ; -> 002F2D60 fn
00463FFE  test     eax, eax
00464000  jne      0x464008  ; -> 00464008
00464002  add      rsp, 0x20
00464006  pop      rbx
00464007  ret      
00464008  and      byte ptr [rbx + 0x248], 0xfe
0046400F  mov      rcx, rbx
00464012  mov      dword ptr [rbx + 0x244], 0
0046401C  call     0x4649a0  ; -> 004649A0 fn
00464021  mov      rcx, rbx
00464024  call     0x377190  ; -> 00377190 fn
00464029  or       byte ptr [rbx + 0x248], 2
00464030  mov      dword ptr [rbx + 0x24c], eax
00464036  mov      eax, 1
0046403B  add      rsp, 0x20
0046403F  pop      rbx
00464040  ret      
```

## 00464B30 (66 B, extent 00464B30-00464B72)

Page context: "he record to '[rbx+0x230]', '00377190' a second index to '[rbx+0x234]', '003D8D70' closes.  Interior anchor '0047BE49' (function '0047BE20').  '00377190' (148 B) is the handle-slot issuer '00463FF0'/'00464B30'/'00464F20'/'0047BE20' call on the '02ADBFE0' table (128 entries x 0x20, '[rax]' zero = free): serial '02ADBFC4' increments (wraps at 0xFFFFFF), packs '(serial<<8)|slot' into '[rax]', stores the caller's pointer at '+8', and links "

```
00464B30  push     rbx
00464B32  sub      rsp, 0x20
00464B36  mov      rbx, rcx
00464B39  call     0x2f2d60  ; -> 002F2D60 fn
00464B3E  test     eax, eax
00464B40  jne      0x464b48  ; -> 00464B48
00464B42  add      rsp, 0x20
00464B46  pop      rbx
00464B47  ret      
00464B48  mov      rcx, rbx
00464B4B  mov      dword ptr [rbx + 0x234], 0
00464B55  call     0x377190  ; -> 00377190 fn
00464B5A  or       byte ptr [rbx + 0x23c], 1
00464B61  mov      dword ptr [rbx + 0x238], eax
00464B67  mov      eax, 1
00464B6C  add      rsp, 0x20
00464B70  pop      rbx
00464B71  ret      
```

## 00465680 (13 B, extent 00465680-0046568D)

Page context: " − 1' for types 1–'0xD1'    (byte map '002F443C' and offsets '002F4380', both jump-table data inside '.text'; '002F40F9'–'002F4124').    **46 distinct arm calls**: 45 per-type routines in '00442550'–'00465680', all frontier, and one arm folded onto the    empty '0016D6A0' ('002F4357'). Unhandled types call '0043ED30' ('002F4364'). 5. It calls '003A3D10' again ('002F436B').  **Three type dispatchers, three roles, one type space.** For an"

```
00465680  mov      eax, 0x80
00465685  or       word ptr [rcx + 0x232], ax
0046568C  ret      
```

## 004D7BF0 (10177 B, extent 004D7BF0-004DA3B1)

Page context: " chain and gives the map — type ''h'' installs '004DF440' and '004E0F70', ''i'' installs '004DCC00' and '004DDDF0', '0xA3' installs '004DB350', '0xA6' and '0xA8' share '004DA8A0', and ''j'' installs '004D7BF0'. **The copied template carries the MPG descriptor verbatim**, which is how the program reaches the packet at all: the builder only re-points the *data* descriptor at what it has just written.  **Not read here:** '002D7FC0', '003B3"

```
004D7BF0  mov      rax, rsp
004D7BF3  mov      qword ptr [rax + 0x10], rdx
004D7BF7  mov      qword ptr [rax + 8], rcx
004D7BFB  push     rbx
004D7BFC  push     rbp
004D7BFD  push     rsi
004D7BFE  push     rdi
004D7BFF  push     r12
004D7C01  push     r13
004D7C03  push     r14
004D7C05  push     r15
004D7C07  sub      rsp, 0x138
004D7C0E  movaps   xmmword ptr [rax - 0x58], xmm6
004D7C12  lea      r12, [rip + 0x1b8d217]  ; -> 02064E30
004D7C19  movaps   xmmword ptr [rax - 0x68], xmm7
004D7C1D  mov      r9, rcx
004D7C20  movaps   xmmword ptr [rax - 0x78], xmm8
004D7C25  xor      r8d, r8d
004D7C28  movaps   xmmword ptr [rax - 0x88], xmm9
004D7C30  movaps   xmmword ptr [rax - 0x98], xmm10
004D7C38  movaps   xmmword ptr [rax - 0xa8], xmm11
004D7C40  movaps   xmmword ptr [rax - 0xb8], xmm12
004D7C48  movaps   xmmword ptr [rax - 0xc8], xmm13
004D7C50  movaps   xmmword ptr [rax - 0xd8], xmm14
004D7C58  movaps   xmmword ptr [rax - 0xe8], xmm15
004D7C60  movzx    eax, word ptr [rip + 0x1b8cea5]  ; -> 02064B0C
004D7C67  add      ax, 0xb
004D7C6B  mov      word ptr [rip + 0x1b8d176], ax  ; -> 02064DE8
004D7C72  cwde     
004D7C73  shl      eax, 4
004D7C76  movsxd   rcx, eax
004D7C79  add      rcx, r12
004D7C7C  call     r9
004D7C7F  movsx    ebx, word ptr [rip + 0x1b8ce86]  ; -> 02064B0C
004D7C86  mov      eax, 0x25e
004D7C8B  movss    xmm3, dword ptr [rip + 0x192aba1]  ; -> 01E02834 [u32 0x00000000]
004D7C93  add      eax, ebx
004D7C95  mov      word ptr [rip + 0x1b8d114], ax  ; -> 02064DB0
004D7C9C  mov      ecx, ebx
004D7C9E  inc      ax
004D7CA1  shl      ecx, 4
004D7CA4  mov      word ptr [rip + 0x1b8d109], ax  ; -> 02064DB4
004D7CAB  movsxd   rax, ecx
004D7CAE  mov      word ptr [rip + 0x1b8d103], bx  ; -> 02064DB8
004D7CB5  movzx    r15d, word ptr [rax + r12 + 0xc]
004D7CBB  lea      eax, [rcx + 0x10]
004D7CBE  movsxd   rcx, eax
004D7CC1  lea      eax, [rbx + 6]
004D7CC4  shl      eax, 4
004D7CC7  mov      word ptr [rip + 0x1b8d105], r15w  ; -> 02064DD4
004D7CCF  movups   xmm15, xmmword ptr [rcx + r12]
004D7CD4  movsxd   rcx, eax
004D7CD7  lea      eax, [rbx + 7]
004D7CDA  shl      eax, 4
004D7CDD  movups   xmmword ptr [rip + 0x1b8ce4b], xmm15  ; -> 02064B30
004D7CE5  movups   xmm1, xmmword ptr [rcx + r12]
004D7CEA  movsxd   rcx, eax
004D7CED  lea      eax, [rbx + 8]
004D7CF0  shl      eax, 4
004D7CF3  shufps   xmm15, xmm15, 0xff
004D7CF8  addss    xmm15, xmm3
004D7CFD  movups   xmm0, xmmword ptr [rcx + r12]
004D7D02  movsxd   rcx, eax
004D7D05  lea      eax, [rbx + 9]
004D7D08  shl      eax, 4
004D7D0B  movups   xmmword ptr [rip + 0x1b8cfce], xmm0  ; -> 02064CE0
004D7D12  movups   xmm0, xmmword ptr [rcx + r12]
004D7D17  movsxd   rcx, eax
004D7D1A  lea      eax, [rbx + 0xa]
004D7D1D  shl      eax, 4
004D7D20  movups   xmmword ptr [rip + 0x1b8cfc9], xmm0  ; -> 02064CF0
004D7D27  movups   xmm0, xmmword ptr [rcx + r12]
004D7D2C  movsxd   rcx, eax
004D7D2F  lea      eax, [rbx + 0x10]
004D7D32  shl      eax, 4
004D7D35  movups   xmmword ptr [rip + 0x1b8cfc4], xmm0  ; -> 02064D00
004D7D3C  movups   xmm0, xmmword ptr [rcx + r12]
004D7D41  movsxd   rcx, eax
004D7D44  lea      eax, [rbx + 0x11]
004D7D47  shl      eax, 4
004D7D4A  movups   xmmword ptr [rip + 0x1b8cfbf], xmm0  ; -> 02064D10
004D7D51  movups   xmm0, xmmword ptr [rcx + r12]
004D7D56  movsxd   rcx, eax
004D7D59  lea      eax, [rbx + 0x14]
004D7D5C  cvtdq2ps xmm1, xmm1
004D7D5F  shl      eax, 4
004D7D62  movups   xmmword ptr [rip + 0x1b8cec7], xmm0  ; -> 02064C30
004D7D69  movups   xmm0, xmmword ptr [rcx + r12]
004D7D6E  movsxd   rcx, eax
004D7D71  movss    dword ptr [rip + 0x1b8ceaa], xmm15  ; -> 02064C24
004D7D7A  movups   xmmword ptr [rip + 0x1b8cebf], xmm0  ; -> 02064C40
004D7D81  movups   xmmword ptr [rsp + 0x50], xmm15
004D7D87  movups   xmmword ptr [rip + 0x1b8ce32], xmm1  ; -> 02064BC0
004D7D8E  movss    xmm6, dword ptr [rcx + r12 + 0xc]
004D7D95  lea      eax, [rbx + 5]
004D7D98  movss    xmm5, dword ptr [rip + 0x4285c0]  ; -> 00900360 [u32 0x7F7FFFFF]
004D7DA0  movzx    r13d, bx
004D7DA4  movss    xmm8, dword ptr [rip + 0x192aa8f]  ; -> 01E0283C [f32 1]
004D7DAD  movzx    ebp, bx
004D7DB0  shl      eax, 4
004D7DB3  xorps    xmm7, xmm7
004D7DB6  movsxd   rcx, eax
004D7DB9  lea      eax, [rbx + 4]
004D7DBC  shl      eax, 4
004D7DBF  movss    dword ptr [rip + 0x1b8ce95], xmm6  ; -> 02064C5C
004D7DC7  addss    xmm6, xmm3
004D7DCB  mov      word ptr [rip + 0x1b8cfee], bx  ; -> 02064DC0
004D7DD2  movups   xmm0, xmmword ptr [rcx + r12]
004D7DD7  movsxd   rcx, eax
004D7DDA  mov      word ptr [rip + 0x1b8d003], bx  ; -> 02064DE4
004D7DE1  movups   xmmword ptr [rip + 0x1b8cde8], xmm0  ; -> 02064BD0
004D7DE8  movzx    eax, word ptr [rcx + r12]
004D7DED  movups   xmm0, xmmword ptr [rcx + r12]
004D7DF2  movzx    edx, word ptr [rcx + r12 + 4]
004D7DF8  mov      word ptr [rip + 0x1b8cfcd], ax  ; -> 02064DCC
004D7DFF  lea      eax, [rbx + 1]
004D7E02  and      dx, ax
004D7E05  mov      word ptr [rip + 0x1b8cfdc], ax  ; -> 02064DE8
004D7E0C  movups   xmmword ptr [rip + 0x1b8cded], xmm0  ; -> 02064C00
004D7E13  lea      eax, [rbx + 0x15]
004D7E16  mov      word ptr [rip + 0x1b8cfb3], dx  ; -> 02064DD0
004D7E1D  movss    dword ptr [rsp + 0x24], xmm6
004D7E23  shl      eax, 4
004D7E26  movsxd   rcx, eax
004D7E29  lea      eax, [rbx + 0x16]
004D7E2C  shl      eax, 4
004D7E2F  movss    dword ptr [rip + 0x1b8ce1d], xmm6  ; -> 02064C54
004D7E37  movups   xmm0, xmmword ptr [rcx + r12]
004D7E3C  movsxd   rcx, eax
004D7E3F  lea      eax, [rbx + 2]
004D7E42  shl      eax, 4
004D7E45  movups   xmmword ptr [rip + 0x1b8cd94], xmm0  ; -> 02064BE0
004D7E4C  movups   xmm0, xmmword ptr [rcx + r12]
004D7E51  movsxd   rcx, eax
004D7E54  lea      eax, [rbx + 3]
004D7E57  shl      eax, 4
004D7E5A  movups   xmmword ptr [rip + 0x1b8cd8f], xmm0  ; -> 02064BF0
004D7E61  movups   xmm0, xmmword ptr [rcx + r12]
004D7E66  movsxd   rcx, eax
004D7E69  movups   xmmword ptr [rip + 0x1b8ce50], xmm0  ; -> 02064CC0
004D7E70  movups   xmm0, xmmword ptr [rcx + r12]
004D7E75  movups   xmmword ptr [rip + 0x1b8ce54], xmm0  ; -> 02064CD0
004D7E7C  cmp      dx, bx
004D7E7F  je       0x4d7ff4  ; -> 004D7FF4
004D7E85  movss    xmm0, dword ptr [rip + 0x1b8cdaf]  ; -> 02064C3C
004D7E8D  ucomiss  xmm0, xmm7
004D7E90  jp       0x4d7e99  ; -> 004D7E99
004D7E92  jne      0x4d7e99  ; -> 004D7E99
004D7E94  movaps   xmm2, xmm5
004D7E97  jmp      0x4d7ea1  ; -> 004D7EA1
004D7E99  movaps   xmm2, xmm8
004D7E9D  divss    xmm2, xmm0
004D7EA1  movss    xmm9, dword ptr [rip + 0x192a986]  ; -> 01E02830 [u32 0x00000000]
004D7EAA  movaps   xmm1, xmm8
004D7EAE  subss    xmm1, xmm0
004D7EB2  movaps   xmm4, xmm9
004D7EB6  addss    xmm4, xmm2
004D7EBA  ucomiss  xmm1, xmm7
004D7EBD  movss    dword ptr [rsp + 0x20], xmm4
004D7EC3  movss    dword ptr [rip + 0x1b8cd75], xmm4  ; -> 02064C40
004D7ECB  movss    dword ptr [rip + 0x1b8cde9], xmm1  ; -> 02064CBC
004D7ED3  jp       0x4d7ee4  ; -> 004D7EE4
004D7ED5  jne      0x4d7ee4  ; -> 004D7EE4
004D7ED7  movss    dword ptr [rip + 0x1b8cc21], xmm5  ; -> 02064B00
004D7EDF  movaps   xmm0, xmm5
004D7EE2  jmp      0x4d7ef4  ; -> 004D7EF4
004D7EE4  movaps   xmm0, xmm8
004D7EE8  divss    xmm0, xmm1
004D7EEC  movss    dword ptr [rip + 0x1b8cc0c], xmm0  ; -> 02064B00
004D7EF4  addss    xmm3, xmm0
004D7EF8  ucomiss  xmm3, xmm7
004D7EFB  movss    dword ptr [rsp + 0x198], xmm3
004D7F04  movss    dword ptr [rip + 0x1b8cd38], xmm3  ; -> 02064C44
004D7F0C  jp       0x4d7f81  ; -> 004D7F81
004D7F0E  jne      0x4d7f81  ; -> 004D7F81
004D7F10  call     0x22cc40  ; -> 0022CC40 fn
004D7F15  movss    xmm3, dword ptr [rip + 0x1b8cd27]  ; -> 02064C44
004D7F1D  movss    xmm0, dword ptr [rip + 0x1b8cd1b]  ; -> 02064C40
004D7F25  movss    xmm15, dword ptr [rip + 0x1b8ccf6]  ; -> 02064C24
004D7F2E  movss    xmm6, dword ptr [rip + 0x1b8cd1e]  ; -> 02064C54
004D7F36  movzx    ebx, word ptr [rip + 0x1b8cbcf]  ; -> 02064B0C
004D7F3D  movss    xmm8, dword ptr [rip + 0x192a8f6]  ; -> 01E0283C [f32 1]
004D7F46  movss    xmm9, dword ptr [rip + 0x192a8e1]  ; -> 01E02830 [u32 0x00000000]
004D7F4F  movzx    r13d, word ptr [rip + 0x1b8ce69]  ; -> 02064DC0
004D7F57  movzx    ebp, word ptr [rip + 0x1b8ce86]  ; -> 02064DE4
004D7F5E  movzx    r15d, word ptr [rip + 0x1b8ce6e]  ; -> 02064DD4
004D7F66  movss    dword ptr [rsp + 0x198], xmm3
004D7F6F  movss    dword ptr [rsp + 0x20], xmm0
004D7F75  movss    dword ptr [rsp + 0x24], xmm6
004D7F7B  movups   xmmword ptr [rsp + 0x50], xmm15
004D7F81  comiss   xmm7, xmm3
004D7F84  jbe      0x4d801c  ; -> 004D801C
004D7F8A  call     0x22cc30  ; -> 0022CC30 fn
004D7F8F  movss    xmm0, dword ptr [rip + 0x1b8ccad]  ; -> 02064C44
004D7F97  movss    xmm3, dword ptr [rip + 0x1b8cca1]  ; -> 02064C40
004D7F9F  movss    xmm15, dword ptr [rip + 0x1b8cc7c]  ; -> 02064C24
004D7FA8  movss    xmm6, dword ptr [rip + 0x1b8cca4]  ; -> 02064C54
004D7FB0  movzx    ebx, word ptr [rip + 0x1b8cb55]  ; -> 02064B0C
004D7FB7  movss    xmm8, dword ptr [rip + 0x192a87c]  ; -> 01E0283C [f32 1]
004D7FC0  movzx    r13d, word ptr [rip + 0x1b8cdf8]  ; -> 02064DC0
004D7FC8  movzx    ebp, word ptr [rip + 0x1b8ce15]  ; -> 02064DE4
004D7FCF  movzx    r15d, word ptr [rip + 0x1b8cdfd]  ; -> 02064DD4
004D7FD7  movss    dword ptr [rsp + 0x198], xmm0
004D7FE0  movss    dword ptr [rsp + 0x20], xmm3
004D7FE6  movss    dword ptr [rsp + 0x24], xmm6
004D7FEC  movups   xmmword ptr [rsp + 0x50], xmm15
004D7FF2  jmp      0x4d8013  ; -> 004D8013
004D7FF4  movss    xmm0, dword ptr [rip + 0x1b8cc48]  ; -> 02064C44
004D7FFC  movss    dword ptr [rsp + 0x198], xmm0
004D8005  movss    xmm0, dword ptr [rip + 0x1b8cc33]  ; -> 02064C40
004D800D  movss    dword ptr [rsp + 0x20], xmm0
004D8013  movss    xmm9, dword ptr [rip + 0x192a814]  ; -> 01E02830 [u32 0x00000000]
004D801C  movss    xmm0, dword ptr [rip + 0x1b8cc9c]  ; -> 02064CC0
004D8024  subss    xmm0, dword ptr [rip + 0x1b8cc9c]  ; -> 02064CC8
004D802C  movss    xmm1, dword ptr [rip + 0x1b8cc90]  ; -> 02064CC4
004D8034  subss    xmm1, dword ptr [rip + 0x1b8cc90]  ; -> 02064CCC
004D803C  movss    xmm2, dword ptr [rip + 0x1b8cc60]  ; -> 02064CA4
004D8044  movss    xmm14, dword ptr [rip + 0x1b8cb9b]  ; -> 02064BE8
004D804D  movss    dword ptr [rip + 0x1b8cc6b], xmm0  ; -> 02064CC0
004D8055  movss    xmm0, dword ptr [rip + 0x1b8cc73]  ; -> 02064CD0
004D805D  mulss    xmm0, dword ptr [rip + 0x1b8cc73]  ; -> 02064CD8
004D8065  movsx    eax, bx
004D8068  add      eax, 0x14
004D806B  movss    dword ptr [rip + 0x1b8cc51], xmm1  ; -> 02064CC4
004D8073  movss    xmm1, dword ptr [rip + 0x1b8cc39]  ; -> 02064CB4
004D807B  shl      eax, 4
004D807E  movss    dword ptr [rip + 0x1b8cc4a], xmm0  ; -> 02064CD0
004D8086  movss    xmm0, dword ptr [rip + 0x1b8cc46]  ; -> 02064CD4
004D808E  mulss    xmm0, dword ptr [rip + 0x1b8cc46]  ; -> 02064CDC
004D8096  movsxd   rcx, eax
004D8099  movss    dword ptr [rsp + 0x28], xmm1
004D809F  movss    dword ptr [rsp + 0x2c], xmm2
004D80A5  movss    dword ptr [rip + 0x1b8cc27], xmm0  ; -> 02064CD4
004D80AD  movzx    eax, word ptr [rcx + r12]
004D80B2  movss    xmm0, dword ptr [rip + 0x1b8cb3a]  ; -> 02064BF4
004D80BA  dec      ax
004D80BD  movzx    r14d, word ptr [rcx + r12 + 4]
004D80C3  xor      esi, esi
004D80C5  movss    dword ptr [rsp + 0x30], xmm0
004D80CB  mov      word ptr [rip + 0x1b8ccf2], ax  ; -> 02064DC4
004D80D2  jmp      0x4d80e6  ; -> 004D80E6
004D80D4  nop      dword ptr [rax]
004D80D8  nop      dword ptr [rax + rax]
004D80E0  movups   xmm15, xmmword ptr [rsp + 0x50]
004D80E6  movss    xmm0, dword ptr [rip + 0x1b8cade]  ; -> 02064BCC
004D80EE  movaps   xmm1, xmm6
004D80F1  movss    xmm5, dword ptr [rip + 0x1b8cae7]  ; -> 02064BE0
004D80F9  movaps   xmm13, xmm14
004D80FD  addss    xmm14, dword ptr [rip + 0x1b8cae6]  ; -> 02064BEC
004D8106  movss    dword ptr [rip + 0x1b8ca6e], xmm0  ; -> 02064B7C
004D810E  add      r14w, -2
004D8113  movss    dword ptr [rip + 0x1b8ca71], xmm0  ; -> 02064B8C
004D811B  movaps   xmm12, xmm9
004D811F  movaps   xmm0, xmm6
004D8122  movsx    edx, r13w
004D8126  movaps   xmm6, xmm15
004D812A  mulss    xmm5, xmm8
004D812F  mov      word ptr [rip + 0x1b8cc91], r14w  ; -> 02064DC8
004D8137  movaps   xmm4, xmm14
004D813B  mulss    xmm13, xmm8
004D8140  lea      eax, [rdx + 0x1e]
004D8143  addss    xmm14, dword ptr [rip + 0x1b8caa0]  ; -> 02064BEC
004D814C  shl      eax, 4
004D814F  addss    xmm12, xmm8
004D8154  movsxd   rcx, eax
004D8157  lea      eax, [rdx + 0x1f]
004D815A  shl      eax, 4
004D815D  cmp      word ptr [rip + 0x1b8cc6c], bx  ; -> 02064DD0
004D8164  movss    dword ptr [rsp + 0x44], xmm14
004D816B  movups   xmm10, xmmword ptr [rcx + r12]
004D8170  movsxd   rcx, eax
004D8173  movss    dword ptr [rip + 0x1b8ca6c], xmm14  ; -> 02064BE8
004D817C  mulss    xmm1, xmm10
004D8181  movups   xmm11, xmmword ptr [rcx + r12]
004D8186  movups   xmmword ptr [rip + 0x1b8ca82], xmm10  ; -> 02064C10
004D818E  mulss    xmm10, dword ptr [rip + 0x1b8ca39]  ; -> 02064BD0
004D8197  maxss    xmm6, xmm1
004D819B  mulss    xmm0, xmm11
004D81A0  movaps   xmm1, xmm15
004D81A4  movups   xmmword ptr [rip + 0x1b8c994], xmm11  ; -> 02064B40
004D81AC  mulss    xmm11, dword ptr [rip + 0x1b8ca1b]  ; -> 02064BD0
004D81B5  addss    xmm10, xmm12
004D81BA  maxss    xmm1, xmm0
004D81BE  mulss    xmm4, xmm8
004D81C3  movss    xmm0, dword ptr [rip + 0x1b8ca4d]  ; -> 02064C18
004D81CB  addss    xmm11, xmm12
004D81D0  minss    xmm10, dword ptr [rip + 0x1b8c9ff]  ; -> 02064BD8
004D81D9  movss    dword ptr [rsp + 0x34], xmm5
004D81DF  movss    dword ptr [rsp + 0x3c], xmm1
004D81E5  movss    xmm1, dword ptr [rip + 0x1b8c9e7]  ; -> 02064BD4
004D81ED  minss    xmm11, dword ptr [rip + 0x1b8c9e2]  ; -> 02064BD8
004D81F6  maxss    xmm10, dword ptr [rip + 0x1b8c9dd]  ; -> 02064BDC
004D81FF  mulss    xmm0, xmm1
004D8203  movss    dword ptr [rsp + 0x40], xmm4
004D8209  maxss    xmm11, dword ptr [rip + 0x1b8c9ca]  ; -> 02064BDC
004D8212  movss    dword ptr [rip + 0x1b8c9fe], xmm0  ; -> 02064C18
004D821A  movaps   xmm14, xmm10
004D821E  movss    xmm0, dword ptr [rip + 0x1b8c9f6]  ; -> 02064C1C
004D8226  movaps   xmm15, xmm10
004D822A  mulss    xmm14, dword ptr [rip + 0x1b8c98d]  ; -> 02064BC0
004D8233  mulss    xmm15, dword ptr [rip + 0x1b8c988]  ; -> 02064BC4
004D823C  mulss    xmm0, xmm1
004D8240  movss    dword ptr [rip + 0x1b8c9c7], xmm10  ; -> 02064C10
004D8249  mulss    xmm10, dword ptr [rip + 0x1b8c976]  ; -> 02064BC8
004D8252  movss    dword ptr [rip + 0x1b8c9c2], xmm0  ; -> 02064C1C
004D825A  movss    xmm0, dword ptr [rip + 0x1b8c8e6]  ; -> 02064B48
004D8262  mulss    xmm0, xmm1
004D8266  movss    dword ptr [rip + 0x1b8c8d1], xmm11  ; -> 02064B40
004D826F  movss    dword ptr [rsp + 0x4c], xmm6
004D8275  movss    dword ptr [rip + 0x1b8c8cb], xmm0  ; -> 02064B48
004D827D  movss    xmm0, dword ptr [rip + 0x1b8c8c7]  ; -> 02064B4C
004D8285  mulss    xmm0, xmm1
004D8289  movaps   xmm1, xmm11
004D828D  mulss    xmm1, dword ptr [rip + 0x1b8c92f]  ; -> 02064BC4
004D8295  movss    dword ptr [rip + 0x1b8c8af], xmm0  ; -> 02064B4C
004D829D  movaps   xmm0, xmm11
004D82A1  mulss    xmm0, dword ptr [rip + 0x1b8c917]  ; -> 02064BC0
004D82A9  mulss    xmm11, dword ptr [rip + 0x1b8c916]  ; -> 02064BC8
004D82B2  movss    dword ptr [rsp + 0x190], xmm0
004D82BB  movss    dword ptr [rsp + 0x38], xmm1
004D82C1  je       0x4d8562  ; -> 004D8562
004D82C7  movss    xmm0, dword ptr [rip + 0x1b8c979]  ; -> 02064C48
004D82CF  movaps   xmm1, xmm5
004D82D2  movaps   xmm3, xmm0
004D82D5  addss    xmm1, xmm9
004D82DA  movaps   xmm2, xmm0
004D82DD  mulss    xmm3, xmm4
004D82E1  movss    xmm4, dword ptr [rsp + 0x2c]
004D82E7  movaps   xmm6, xmm5
004D82EA  movaps   xmm0, xmm4
004D82ED  mulss    xmm2, xmm13
004D82F2  mulss    xmm0, xmm4
004D82F6  addss    xmm6, xmm9
004D82FB  movss    xmm4, dword ptr [rsp + 0x28]
004D8301  movss    dword ptr [rip + 0x1b8c9af], xmm3  ; -> 02064CB8
004D8309  movss    dword ptr [rip + 0x1b8c973], xmm0  ; -> 02064C84
004D8311  movaps   xmm0, xmm4
004D8314  mulss    xmm3, xmm3
004D8318  mulss    xmm0, xmm4
004D831C  mulss    xmm1, xmm1
004D8320  movss    dword ptr [rip + 0x1b8c96c], xmm0  ; -> 02064C94
004D8328  movss    dword ptr [rip + 0x1b8c968], xmm3  ; -> 02064C98
004D8330  mulss    xmm3, xmm8
004D8335  movss    dword ptr [rip + 0x1b8c96b], xmm2  ; -> 02064CA8
004D833D  mulss    xmm6, xmm6
004D8341  mulss    xmm2, xmm2
004D8345  movss    dword ptr [rip + 0x1b8c943], xmm1  ; -> 02064C90
004D834D  mulss    xmm1, xmm8
004D8352  movss    dword ptr [rip + 0x1b8c926], xmm6  ; -> 02064C80
004D835A  movss    dword ptr [rip + 0x1b8c926], xmm2  ; -> 02064C88
004D8362  addss    xmm3, xmm1
004D8366  mulss    xmm2, xmm8
004D836B  mulss    xmm6, xmm8
004D8370  cvtps2pd xmm0, xmm3
004D8373  addss    xmm6, xmm2
004D8377  movss    dword ptr [rip + 0x1b8c91d], xmm3  ; -> 02064C9C
004D837F  andps    xmm0, xmmword ptr [rip + 0x18139fa]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004D8386  cvtpd2ps xmm0, xmm0
004D838A  movss    dword ptr [rip + 0x1b8c8fa], xmm6  ; -> 02064C8C
004D8392  call     0x861f14  ; -> 00861F14 fn
004D8397  cvtps2pd xmm1, xmm6
004D839A  movss    dword ptr [rsp + 0x48], xmm0
004D83A0  andps    xmm1, xmmword ptr [rip + 0x18139d9]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004D83A7  cvtpd2ps xmm0, xmm1
004D83AB  call     0x861f14  ; -> 00861F14 fn
004D83B0  movss    xmm3, dword ptr [rip + 0x1b8c884]  ; -> 02064C3C
004D83B8  movaps   xmm1, xmm0
004D83BB  addss    xmm1, xmm9
004D83C0  mulss    xmm1, dword ptr [rip + 0x1b8c884]  ; -> 02064C4C
004D83C8  ucomiss  xmm3, xmm1
004D83CB  jp       0x4d83d4  ; -> 004D83D4
004D83CD  mov      eax, 1
004D83D2  je       0x4d83d6  ; -> 004D83D6
004D83D4  mov      eax, esi
004D83D6  movss    xmm4, dword ptr [rip + 0x1b8c856]  ; -> 02064C34
004D83DE  lea      edx, [rbx + 0x10]
004D83E1  movss    xmm5, dword ptr [rip + 0x1b8c847]  ; -> 02064C30
004D83E9  mov      ecx, esi
004D83EB  movss    xmm6, dword ptr [rsp + 0x198]
004D83F4  comiss   xmm1, xmm3
004D83F7  seta     cl
004D83FA  shl      cx, 4
004D83FE  add      cx, ax
004D8401  movzx    eax, dx
004D8404  and      ax, cx
004D8407  cmp      ax, bx
004D840A  jne      0x4d8431  ; -> 004D8431
004D840C  mulss    xmm1, dword ptr [rsp + 0x20]
004D8412  movaps   xmm0, xmm4
004D8415  subss    xmm0, xmm5
004D8419  movss    dword ptr [rsp + 0x2c], xmm0
004D841F  movss    dword ptr [rip + 0x1b8c87d], xmm0  ; -> 02064CA4
004D8427  mulss    xmm0, xmm1
004D842B  addss    xmm0, xmm5
004D842F  jmp      0x4d8455  ; -> 004D8455
004D8431  movss    xmm0, dword ptr [rip + 0x1b8c7ff]  ; -> 02064C38
004D8439  subss    xmm1, xmm3
004D843D  subss    xmm0, xmm4
004D8441  mulss    xmm1, xmm6
004D8445  movss    dword ptr [rip + 0x1b8c85b], xmm0  ; -> 02064CA8
004D844D  mulss    xmm0, xmm1
004D8451  addss    xmm0, xmm4
004D8455  movss    dword ptr [rip + 0x1b8c843], xmm0  ; -> 02064CA0
004D845D  movss    xmm2, dword ptr [rip + 0x1b8c767]  ; -> 02064BCC
004D8465  movaps   xmm1, xmm9
004D8469  addss    xmm1, dword ptr [rsp + 0x48]
004D846F  mulss    xmm2, xmm0
004D8473  mulss    xmm1, dword ptr [rip + 0x1b8c7d1]  ; -> 02064C4C
004D847B  ucomiss  xmm3, xmm1
004D847E  jp       0x4d8487  ; -> 004D8487
004D8480  mov      ecx, 1
004D8485  je       0x4d8489  ; -> 004D8489
004D8487  mov      ecx, esi
004D8489  comiss   xmm1, xmm3
004D848C  mov      eax, esi
004D848E  seta     al
004D8491  shl      ax, 4
004D8495  add      ax, cx
004D8498  and      dx, ax
004D849B  mov      word ptr [rip + 0x1b8c66e], ax  ; -> 02064B10
004D84A2  mov      word ptr [rip + 0x1b8c93f], dx  ; -> 02064DE8
004D84A9  cmp      dx, bx
004D84AC  jne      0x4d84d3  ; -> 004D84D3
004D84AE  mulss    xmm1, dword ptr [rsp + 0x20]
004D84B4  movaps   xmm0, xmm4
004D84B7  subss    xmm0, xmm5
004D84BB  movss    dword ptr [rsp + 0x28], xmm0
004D84C1  movss    dword ptr [rip + 0x1b8c7eb], xmm0  ; -> 02064CB4
004D84C9  mulss    xmm0, xmm1
004D84CD  addss    xmm0, xmm5
004D84D1  jmp      0x4d84f7  ; -> 004D84F7
004D84D3  movss    xmm0, dword ptr [rip + 0x1b8c75d]  ; -> 02064C38
004D84DB  subss    xmm1, xmm3
004D84DF  subss    xmm0, xmm4
004D84E3  mulss    xmm1, xmm6
004D84E7  movss    dword ptr [rip + 0x1b8c7c9], xmm0  ; -> 02064CB8
004D84EF  mulss    xmm0, xmm1
004D84F3  addss    xmm0, xmm4
004D84F7  movss    dword ptr [rip + 0x1b8c7b1], xmm0  ; -> 02064CB0
004D84FF  movss    xmm1, dword ptr [rip + 0x1b8c6c5]  ; -> 02064BCC
004D8507  mulss    xmm1, xmm0
004D850B  mov      dword ptr [rip + 0x1b8c5ef], 0x437f0000  ; -> 02064B04
004D8515  movss    xmm0, dword ptr [rip + 0x3ed623]  ; -> 008C5B40 [f32 255]
004D851D  comiss   xmm0, xmm2
004D8520  ja       0x4d8525  ; -> 004D8525
004D8522  movaps   xmm2, xmm0
004D8525  comiss   xmm0, xmm1
004D8528  ja       0x4d852d  ; -> 004D852D
004D852A  movaps   xmm1, xmm0
004D852D  movss    xmm0, dword ptr [rsp + 0x190]
004D8536  maxss    xmm1, xmm9
004D853B  movss    xmm6, dword ptr [rsp + 0x4c]
004D8541  maxss    xmm2, xmm9
004D8546  movss    xmm5, dword ptr [rsp + 0x34]
004D854C  movss    dword ptr [rip + 0x1b8c638], xmm1  ; -> 02064B8C
004D8554  movss    xmm1, dword ptr [rsp + 0x38]
004D855A  movss    dword ptr [rip + 0x1b8c61a], xmm2  ; -> 02064B7C
004D8562  movss    xmm2, dword ptr [rip + 0x1b8c69e]  ; -> 02064C08
004D856A  minss    xmm0, xmm2
004D856E  shufps   xmm5, xmm5, 0
004D8572  minss    xmm1, xmm2
004D8576  minss    xmm14, xmm2
004D857B  minss    xmm15, xmm2
004D8580  minss    xmm10, xmm2
004D8585  movss    dword ptr [rsp + 0x190], xmm0
004D858E  minss    xmm11, xmm2
004D8593  movups   xmm0, xmmword ptr [rip + 0x1b8c746]  ; -> 02064CE0
004D859A  movss    dword ptr [rsp + 0x38], xmm1
004D85A0  movss    xmm1, dword ptr [rip + 0x1b8c750]  ; -> 02064CF8
004D85A8  mulps    xmm5, xmm0
004D85AB  movss    xmm0, dword ptr [rip + 0x1b8c73d]  ; -> 02064CF0
004D85B3  mulss    xmm0, xmm6
004D85B7  mulss    xmm1, xmm6
004D85BB  movups   xmmword ptr [rip + 0x1b8c55e], xmm5  ; -> 02064B20
004D85C2  movss    xmm2, dword ptr [rip + 0x1b8c55a]  ; -> 02064B24
004D85CA  addss    xmm5, xmm0
004D85CE  movss    xmm0, dword ptr [rip + 0x1b8c71e]  ; -> 02064CF4
004D85D6  movss    xmm3, dword ptr [rip + 0x1b8c54a]  ; -> 02064B28
004D85DE  movss    xmm4, dword ptr [rip + 0x1b8c546]  ; -> 02064B2C
004D85E6  addss    xmm3, xmm1
004D85EA  movss    xmm1, dword ptr [rip + 0x1b8c712]  ; -> 02064D04
004D85F2  mulss    xmm0, xmm6
004D85F6  mulss    xmm1, xmm13
004D85FB  addss    xmm2, xmm0
004D85FF  movss    xmm0, dword ptr [rip + 0x1b8c6f5]  ; -> 02064CFC
004D8607  mulss    xmm0, xmm6
004D860B  addss    xmm4, xmm0
004D860F  movss    xmm0, dword ptr [rip + 0x1b8c6e9]  ; -> 02064D00
004D8617  mulss    xmm0, xmm13
004D861C  addss    xmm2, xmm1
004D8620  movss    xmm1, dword ptr [rip + 0x1b8c6e4]  ; -> 02064D0C
004D8628  mulss    xmm1, xmm13
004D862D  addss    xmm5, xmm0
004D8631  movss    xmm0, dword ptr [rip + 0x1b8c6cf]  ; -> 02064D08
004D8639  mulss    xmm0, xmm13
004D863E  movss    xmm13, dword ptr [rip + 0x1b8c6d5]  ; -> 02064D1C
004D8647  addss    xmm4, xmm1
004D864B  movss    xmm1, dword ptr [rip + 0x1b8c6c1]  ; -> 02064D14
004D8653  addss    xmm3, xmm0
004D8657  mulss    xmm1, xmm12
004D865C  movss    xmm0, dword ptr [rip + 0x1b8c6ac]  ; -> 02064D10
004D8664  mulss    xmm0, xmm12
004D8669  addss    xmm1, xmm2
004D866D  addss    xmm0, xmm5
004D8671  movss    dword ptr [rip + 0x1b8c4db], xmm1  ; -> 02064B54
004D8679  movaps   xmm1, xmm13
004D867D  mulss    xmm1, xmm12
004D8682  movss    dword ptr [rip + 0x1b8c4c6], xmm0  ; -> 02064B50
004D868A  movss    xmm0, dword ptr [rip + 0x1b8c686]  ; -> 02064D18
004D8692  addss    xmm1, xmm4
004D8696  mulss    xmm0, xmm12
004D869B  addss    xmm0, xmm3
004D869F  ucomiss  xmm1, xmm7
004D86A2  movss    dword ptr [rip + 0x1b8c4ae], xmm0  ; -> 02064B58
004D86AA  movss    dword ptr [rip + 0x1b8c4aa], xmm1  ; -> 02064B5C
004D86B2  jp       0x4d86c0  ; -> 004D86C0
004D86B4  jne      0x4d86c0  ; -> 004D86C0
004D86B6  movss    xmm6, dword ptr [rip + 0x427ca2]  ; -> 00900360 [u32 0x7F7FFFFF]
004D86BE  jmp      0x4d86c8  ; -> 004D86C8
004D86C0  movaps   xmm6, xmm8
004D86C4  divss    xmm6, xmm1
004D86C8  movss    xmm2, dword ptr [rip + 0x1b8c53c]  ; -> 02064C0C
004D86D0  movss    xmm4, dword ptr [rsp + 0x3c]
004D86D6  maxss    xmm10, xmm2
004D86DB  movss    xmm0, dword ptr [rsp + 0x190]
004D86E4  maxss    xmm14, xmm2
004D86E9  movss    xmm1, dword ptr [rsp + 0x38]
004D86EF  maxss    xmm0, xmm2
004D86F3  movss    xmm5, dword ptr [rsp + 0x34]
004D86F9  maxss    xmm1, xmm2
004D86FD  shufps   xmm5, xmm5, 0
004D8701  maxss    xmm15, xmm2
004D8706  maxss    xmm11, xmm2
004D870B  movss    dword ptr [rip + 0x1b8c464], xmm10  ; -> 02064B78
004D8714  movss    xmm10, dword ptr [rsp + 0x40]
004D871B  movss    dword ptr [rip + 0x1b8c45d], xmm0  ; -> 02064B80
004D8723  movups   xmm0, xmmword ptr [rip + 0x1b8c5b6]  ; -> 02064CE0
004D872A  movss    dword ptr [rip + 0x1b8c452], xmm1  ; -> 02064B84
004D8732  movss    xmm1, dword ptr [rip + 0x1b8c5be]  ; -> 02064CF8
004D873A  mulps    xmm5, xmm0
004D873D  movss    xmm0, dword ptr [rip + 0x1b8c5ab]  ; -> 02064CF0
004D8745  mulss    xmm0, xmm4
004D8749  mulss    xmm1, xmm4
004D874D  movups   xmmword ptr [rip + 0x1b8c3cc], xmm5  ; -> 02064B20
004D8754  movss    xmm2, dword ptr [rip + 0x1b8c3c8]  ; -> 02064B24
004D875C  addss    xmm5, xmm0
004D8760  movss    xmm0, dword ptr [rip + 0x1b8c58c]  ; -> 02064CF4
004D8768  movss    xmm3, dword ptr [rip + 0x1b8c3b8]  ; -> 02064B28
004D8770  mulss    xmm0, xmm4
004D8774  addss    xmm3, xmm1
004D8778  movss    xmm1, dword ptr [rip + 0x1b8c584]  ; -> 02064D04
004D8780  mulss    xmm1, xmm10
004D8785  addss    xmm2, xmm0
004D8789  movss    dword ptr [rip + 0x1b8c3de], xmm14  ; -> 02064B70
004D8792  movss    xmm0, dword ptr [rip + 0x1b8c562]  ; -> 02064CFC
004D879A  mulss    xmm0, xmm4
004D879E  movss    xmm4, dword ptr [rip + 0x1b8c386]  ; -> 02064B2C
004D87A6  addss    xmm2, xmm1
004D87AA  movss    dword ptr [rip + 0x1b8c3c1], xmm15  ; -> 02064B74
004D87B3  movss    xmm1, dword ptr [rip + 0x1b8c551]  ; -> 02064D0C
004D87BB  addss    xmm4, xmm0
004D87BF  movss    xmm0, dword ptr [rip + 0x1b8c539]  ; -> 02064D00
004D87C7  mulss    xmm0, xmm10
004D87CC  mulss    xmm1, xmm10
004D87D1  addss    xmm5, xmm0
004D87D5  movss    dword ptr [rip + 0x1b8c3aa], xmm11  ; -> 02064B88
004D87DE  movss    xmm0, dword ptr [rip + 0x1b8c522]  ; -> 02064D08
004D87E6  mulss    xmm0, xmm10
004D87EB  addss    xmm4, xmm1
004D87EF  movss    xmm1, dword ptr [rip + 0x1b8c51d]  ; -> 02064D14
004D87F7  mulss    xmm1, xmm12
004D87FC  addss    xmm3, xmm0
004D8800  movss    dword ptr [rip + 0x1b8c318], xmm5  ; -> 02064B20
004D8808  movss    xmm0, dword ptr [rip + 0x1b8c500]  ; -> 02064D10
004D8810  mulss    xmm0, xmm12
004D8815  addss    xmm1, xmm2
004D8819  movss    dword ptr [rip + 0x1b8c303], xmm2  ; -> 02064B24
004D8821  movss    dword ptr [rip + 0x1b8c2ff], xmm3  ; -> 02064B28
004D8829  addss    xmm0, xmm5
004D882D  movss    dword ptr [rip + 0x1b8c2f7], xmm4  ; -> 02064B2C
004D8835  movss    dword ptr [rip + 0x1b8c327], xmm1  ; -> 02064B64
004D883D  movaps   xmm5, xmm13
004D8841  movups   xmm1, xmmword ptr [rip + 0x1b8c308]  ; -> 02064B50
004D8848  mulss    xmm5, xmm12
004D884D  movss    dword ptr [rip + 0x1b8c30b], xmm0  ; -> 02064B60
004D8855  movss    xmm0, dword ptr [rip + 0x1b8c4bb]  ; -> 02064D18
004D885D  mulss    xmm0, xmm12
004D8862  addss    xmm5, xmm4
004D8866  addss    xmm0, xmm3
004D886A  movss    dword ptr [rip + 0x1b8c2fa], xmm5  ; -> 02064B6C
004D8872  movss    dword ptr [rip + 0x1b8c2ee], xmm0  ; -> 02064B68
004D887A  movups   xmm0, xmmword ptr [rip + 0x1b8c2ef]  ; -> 02064B70
004D8881  cvttps2dq xmm10, xmm0
004D8886  movups   xmm0, xmmword ptr [rip + 0x1b8c2f3]  ; -> 02064B80
004D888D  movups   xmmword ptr [rip + 0x1b8c2db], xmm10  ; -> 02064B70
004D8895  cvttps2dq xmm12, xmm0
004D889A  movaps   xmm0, xmm6
004D889D  shufps   xmm0, xmm0, 0
004D88A1  mulps    xmm1, xmm0
004D88A4  movaps   xmm0, xmm6
004D88A7  movups   xmmword ptr [rip + 0x1b8c2d1], xmm12  ; -> 02064B80
004D88AF  movups   xmmword ptr [rip + 0x1b8c29a], xmm1  ; -> 02064B50
004D88B6  ucomiss  xmm5, xmm7
004D88B9  movups   xmm1, xmmword ptr [rip + 0x1b8c2e0]  ; -> 02064BA0
004D88C0  shufps   xmm0, xmm0, 0
004D88C4  mulps    xmm1, xmm0
004D88C7  movups   xmmword ptr [rip + 0x1b8c2d2], xmm1  ; -> 02064BA0
004D88CE  jp       0x4d88dc  ; -> 004D88DC
004D88D0  jne      0x4d88dc  ; -> 004D88DC
004D88D2  movss    xmm2, dword ptr [rip + 0x427a86]  ; -> 00900360 [u32 0x7F7FFFFF]
004D88DA  jmp      0x4d88e4  ; -> 004D88E4
004D88DC  movaps   xmm2, xmm8
004D88E0  divss    xmm2, xmm5
004D88E4  cmp      word ptr [rip + 0x1b8c4e1], bx  ; -> 02064DCC
004D88EB  movaps   xmm0, xmm2
004D88EE  movups   xmm1, xmmword ptr [rip + 0x1b8c26b]  ; -> 02064B60
004D88F5  shufps   xmm0, xmm0, 0
004D88F9  mulps    xmm1, xmm0
004D88FC  movaps   xmm0, xmm2
004D88FF  shufps   xmm0, xmm0, 0
004D8903  movss    dword ptr [rip + 0x1b8c1f5], xmm2  ; -> 02064B00
004D890B  movups   xmmword ptr [rip + 0x1b8c24e], xmm1  ; -> 02064B60
004D8912  movups   xmm1, xmmword ptr [rip + 0x1b8c297]  ; -> 02064BB0
004D8919  mulps    xmm1, xmm0
004D891C  movups   xmmword ptr [rip + 0x1b8c28d], xmm1  ; -> 02064BB0
004D8923  jne      0x4d899c  ; -> 004D899C
004D8925  movss    xmm11, dword ptr [rsp + 0x30]
004D892C  movss    xmm2, dword ptr [rip + 0x1b8c2bc]  ; -> 02064BF0
004D8934  movaps   xmm3, xmm11
004D8938  addss    xmm11, dword ptr [rip + 0x1b8c2bb]  ; -> 02064BFC
004D8941  movss    xmm6, dword ptr [rip + 0x1929eef]  ; -> 01E02838 [u32 0x00000000]
004D8949  movss    xmm14, dword ptr [rsp + 0x44]
004D8950  movaps   xmm0, xmm6
004D8953  addss    xmm0, xmm8
004D8958  mulss    xmm2, xmm8
004D895D  movaps   xmm1, xmm11
004D8961  mulss    xmm3, xmm8
004D8966  addss    xmm11, dword ptr [rip + 0x1b8c28d]  ; -> 02064BFC
004D896F  movss    dword ptr [rip + 0x1b8c231], xmm0  ; -> 02064BA8
004D8977  movaps   xmm4, xmm2
004D897A  movss    dword ptr [rip + 0x1b8c236], xmm0  ; -> 02064BB8
004D8982  mulss    xmm1, xmm8
004D8987  movss    dword ptr [rsp + 0x30], xmm11
004D898E  movss    dword ptr [rip + 0x1b8c25d], xmm11  ; -> 02064BF4
004D8997  jmp      0x4d8b7f  ; -> 004D8B7F
004D899C  movss    xmm1, dword ptr [rip + 0x1b8c1ac]  ; -> 02064B50
004D89A4  subss    xmm1, dword ptr [rip + 0x1b8c314]  ; -> 02064CC0
004D89AC  movss    xmm0, dword ptr [rip + 0x1b8c1a0]  ; -> 02064B54
004D89B4  subss    xmm0, dword ptr [rip + 0x1b8c308]  ; -> 02064CC4
004D89BC  ucomiss  xmm1, xmm7
004D89BF  movss    dword ptr [rip + 0x1b8c1d9], xmm1  ; -> 02064BA0
004D89C7  movss    dword ptr [rip + 0x1b8c1d5], xmm0  ; -> 02064BA4
004D89CF  jp       0x4d89d3  ; -> 004D89D3
004D89D1  je       0x4d89da  ; -> 004D89DA
004D89D3  ucomiss  xmm0, xmm7
004D89D6  jp       0x4d89ef  ; -> 004D89EF
004D89D8  jne      0x4d89ef  ; -> 004D89EF
004D89DA  call     0x22cc40  ; -> 0022CC40 fn
004D89DF  movss    xmm0, dword ptr [rip + 0x1b8c1bd]  ; -> 02064BA4
004D89E7  movss    xmm1, dword ptr [rip + 0x1b8c1b1]  ; -> 02064BA0
004D89EF  comiss   xmm7, xmm1
004D89F2  ja       0x4d89f9  ; -> 004D89F9
004D89F4  comiss   xmm7, xmm0
004D89F7  jbe      0x4d89fe  ; -> 004D89FE
004D89F9  call     0x22cc30  ; -> 0022CC30 fn
004D89FE  call     0x22cc20  ; -> 0022CC20 fn
004D8A03  movss    xmm1, dword ptr [rip + 0x1b8c155]  ; -> 02064B60
004D8A0B  subss    xmm1, dword ptr [rip + 0x1b8c2ad]  ; -> 02064CC0
004D8A13  movss    xmm0, dword ptr [rip + 0x1b8c149]  ; -> 02064B64
004D8A1B  subss    xmm0, dword ptr [rip + 0x1b8c2a1]  ; -> 02064CC4
004D8A23  ucomiss  xmm1, xmm7
004D8A26  movss    dword ptr [rip + 0x1b8c182], xmm1  ; -> 02064BB0
004D8A2E  movss    dword ptr [rip + 0x1b8c17e], xmm0  ; -> 02064BB4
004D8A36  jp       0x4d8a3a  ; -> 004D8A3A
004D8A38  je       0x4d8a41  ; -> 004D8A41
004D8A3A  ucomiss  xmm0, xmm7
004D8A3D  jp       0x4d8a56  ; -> 004D8A56
004D8A3F  jne      0x4d8a56  ; -> 004D8A56
004D8A41  call     0x22cc40  ; -> 0022CC40 fn
004D8A46  movss    xmm0, dword ptr [rip + 0x1b8c166]  ; -> 02064BB4
004D8A4E  movss    xmm1, dword ptr [rip + 0x1b8c15a]  ; -> 02064BB0
004D8A56  comiss   xmm7, xmm1
004D8A59  ja       0x4d8a60  ; -> 004D8A60
004D8A5B  comiss   xmm7, xmm0
004D8A5E  jbe      0x4d8a65  ; -> 004D8A65
004D8A60  call     0x22cc30  ; -> 0022CC30 fn
004D8A65  call     0x22cc20  ; -> 0022CC20 fn
004D8A6A  movss    xmm6, dword ptr [rip + 0x1929dc6]  ; -> 01E02838 [u32 0x00000000]
004D8A72  movss    xmm8, dword ptr [rip + 0x1929dc1]  ; -> 01E0283C [f32 1]
004D8A7B  movaps   xmm0, xmm6
004D8A7E  movss    xmm2, dword ptr [rip + 0x1b8c11a]  ; -> 02064BA0
004D8A86  addss    xmm0, xmm8
004D8A8B  movss    xmm3, dword ptr [rip + 0x1b8c111]  ; -> 02064BA4
004D8A93  movss    xmm4, dword ptr [rip + 0x1b8c115]  ; -> 02064BB0
004D8A9B  movss    xmm1, dword ptr [rip + 0x1b8c111]  ; -> 02064BB4
004D8AA3  movss    xmm5, dword ptr [rip + 0x1b8c1a9]  ; -> 02064C54
004D8AAB  mulss    xmm2, dword ptr [rip + 0x1b8c21d]  ; -> 02064CD0
004D8AB3  movzx    ebx, word ptr [rip + 0x1b8c052]  ; -> 02064B0C
004D8ABA  mulss    xmm3, dword ptr [rip + 0x1b8c212]  ; -> 02064CD4
004D8AC2  movzx    r13d, word ptr [rip + 0x1b8c2f6]  ; -> 02064DC0
004D8ACA  mulss    xmm4, dword ptr [rip + 0x1b8c1fe]  ; -> 02064CD0
004D8AD2  movzx    ebp, word ptr [rip + 0x1b8c30b]  ; -> 02064DE4
004D8AD9  mulss    xmm1, dword ptr [rip + 0x1b8c1f3]  ; -> 02064CD4
004D8AE1  movzx    r14d, word ptr [rip + 0x1b8c2df]  ; -> 02064DC8
004D8AE9  movss    xmm9, dword ptr [rip + 0x1929d3e]  ; -> 01E02830 [u32 0x00000000]
004D8AF2  movss    xmm14, dword ptr [rip + 0x1b8c0ed]  ; -> 02064BE8
004D8AFB  movzx    r15d, word ptr [rip + 0x1b8c2d1]  ; -> 02064DD4
004D8B03  movups   xmm10, xmmword ptr [rip + 0x1b8c065]  ; -> 02064B70
004D8B0B  movups   xmm12, xmmword ptr [rip + 0x1b8c06d]  ; -> 02064B80
004D8B13  movss    dword ptr [rip + 0x1b8c08d], xmm0  ; -> 02064BA8
004D8B1B  movss    dword ptr [rip + 0x1b8c095], xmm0  ; -> 02064BB8
004D8B23  movss    xmm0, dword ptr [rip + 0x1b8c0f9]  ; -> 02064C24
004D8B2B  movups   xmmword ptr [rsp + 0x50], xmm0
004D8B30  movss    xmm0, dword ptr [rip + 0x1b8c10c]  ; -> 02064C44
004D8B38  movss    dword ptr [rsp + 0x198], xmm0
004D8B41  movss    xmm0, dword ptr [rip + 0x1b8c0f7]  ; -> 02064C40
004D8B49  movss    dword ptr [rsp + 0x20], xmm0
004D8B4F  movss    xmm0, dword ptr [rip + 0x1b8c09d]  ; -> 02064BF4
004D8B57  movss    dword ptr [rsp + 0x30], xmm0
004D8B5D  movss    xmm0, dword ptr [rip + 0x1b8c14f]  ; -> 02064CB4
004D8B65  movss    dword ptr [rsp + 0x28], xmm0
004D8B6B  movss    xmm0, dword ptr [rip + 0x1b8c131]  ; -> 02064CA4
004D8B73  movss    dword ptr [rsp + 0x2c], xmm0
004D8B79  movss    dword ptr [rsp + 0x24], xmm5
004D8B7F  addss    xmm2, dword ptr [rip + 0x1b8c091]  ; -> 02064C18
004D8B87  addss    xmm3, dword ptr [rip + 0x1b8c08d]  ; -> 02064C1C
004D8B8F  addss    xmm4, dword ptr [rip + 0x1b8bfb1]  ; -> 02064B48
004D8B97  addss    xmm1, dword ptr [rip + 0x1b8bfad]  ; -> 02064B4C
004D8B9F  movss    xmm5, dword ptr [rip + 0x1b8bfa9]  ; -> 02064B50
004D8BA7  movss    xmm15, dword ptr [rip + 0x1b8bf80]  ; -> 02064B30
004D8BB0  ucomiss  xmm15, xmm5
004D8BB4  movss    dword ptr [rip + 0x1b8bfe4], xmm2  ; -> 02064BA0
004D8BBC  movss    dword ptr [rip + 0x1b8bfe0], xmm3  ; -> 02064BA4
004D8BC4  movss    dword ptr [rip + 0x1b8bfe4], xmm4  ; -> 02064BB0
004D8BCC  movss    dword ptr [rip + 0x1b8bfe0], xmm1  ; -> 02064BB4
004D8BD4  jp       0x4d8bde  ; -> 004D8BDE
004D8BD6  mov      r8d, 1
004D8BDC  je       0x4d8be1  ; -> 004D8BE1
004D8BDE  mov      r8d, esi
004D8BE1  movss    xmm4, dword ptr [rip + 0x1b8bf6b]  ; -> 02064B54
004D8BE9  movss    xmm11, dword ptr [rip + 0x1b8bf42]  ; -> 02064B34
004D8BF2  ucomiss  xmm11, xmm4
004D8BF6  jp       0x4d8bff  ; -> 004D8BFF
004D8BF8  mov      edx, 1
004D8BFD  je       0x4d8c01  ; -> 004D8C01
004D8BFF  mov      edx, esi
004D8C01  movss    xmm3, dword ptr [rip + 0x1b8bf4f]  ; -> 02064B58
004D8C09  movss    xmm13, dword ptr [rip + 0x1b8bf26]  ; -> 02064B38
004D8C12  ucomiss  xmm13, xmm3
004D8C16  jp       0x4d8c1f  ; -> 004D8C1F
004D8C18  mov      ecx, 1
004D8C1D  je       0x4d8c21  ; -> 004D8C21
004D8C1F  mov      ecx, esi
004D8C21  comiss   xmm5, xmm15
004D8C25  mov      eax, esi
004D8C27  movsx    edi, bp
004D8C2A  mov      r11d, esi
004D8C2D  seta     r11b
004D8C31  add      r11w, r11w
004D8C35  comiss   xmm4, xmm11
004D8C39  seta     al
004D8C3C  add      r11w, ax
004D8C40  mov      eax, esi
004D8C42  add      r11w, r11w
004D8C46  comiss   xmm3, xmm13
004D8C4A  seta     al
004D8C4D  add      r11w, ax
004D8C51  lea      eax, [rdi + 0x37f]
004D8C57  shl      r11w, 2
004D8C5C  add      r11w, r8w
004D8C60  shl      eax, 4
004D8C63  add      r11w, r11w
004D8C67  add      r11w, dx
004D8C6B  add      r11w, r11w
004D8C6F  add      r11w, cx
004D8C73  movsxd   rcx, eax
004D8C76  add      r11w, r11w
004D8C7A  ucomiss  xmm5, xmm9
004D8C7E  mov      word ptr [rip + 0x1b8be8a], r11w  ; -> 02064B10
004D8C86  movups   xmmword ptr [rcx + r12], xmm10
004D8C8B  jp       0x4d8c95  ; -> 004D8C95
004D8C8D  mov      r8d, 1
004D8C93  je       0x4d8c98  ; -> 004D8C98
004D8C95  mov      r8d, esi
004D8C98  movss    xmm10, dword ptr [rip + 0x1929b93]  ; -> 01E02834 [u32 0x00000000]
004D8CA1  ucomiss  xmm4, xmm10
004D8CA5  jp       0x4d8cae  ; -> 004D8CAE
004D8CA7  mov      edx, 1
004D8CAC  je       0x4d8cb0  ; -> 004D8CB0
004D8CAE  mov      edx, esi
004D8CB0  ucomiss  xmm3, xmm6
004D8CB3  jp       0x4d8cbc  ; -> 004D8CBC
004D8CB5  mov      ecx, 1
004D8CBA  je       0x4d8cbe  ; -> 004D8CBE
004D8CBC  mov      ecx, esi
004D8CBE  movss    xmm2, dword ptr [rip + 0x1b8be9a]  ; -> 02064B60
004D8CC6  mov      eax, esi
004D8CC8  comiss   xmm9, xmm5
004D8CCC  mov      r10d, esi
004D8CCF  seta     r10b
004D8CD3  add      r10w, r10w
004D8CD7  comiss   xmm10, xmm4
004D8CDB  seta     al
004D8CDE  add      r10w, ax
004D8CE2  mov      eax, esi
004D8CE4  add      r10w, r10w
004D8CE8  comiss   xmm6, xmm3
004D8CEB  seta     al
004D8CEE  add      r10w, ax
004D8CF2  lea      eax, [rdi + 0x382]
004D8CF8  shl      r10w, 2
004D8CFD  add      r10w, r8w
004D8D01  shl      eax, 4
004D8D04  add      r10w, r10w
004D8D08  add      r10w, dx
004D8D0C  add      r10w, r10w
004D8D10  add      r10w, cx
004D8D14  movsxd   rcx, eax
004D8D17  add      r10w, r10w
004D8D1B  ucomiss  xmm15, xmm2
004D8D1F  mov      word ptr [rip + 0x1b8bdeb], r10w  ; -> 02064B12
004D8D27  movups   xmmword ptr [rcx + r12], xmm12
004D8D2C  jp       0x4d8d36  ; -> 004D8D36
004D8D2E  mov      r8d, 1
004D8D34  je       0x4d8d39  ; -> 004D8D39
004D8D36  mov      r8d, esi
004D8D39  movss    xmm1, dword ptr [rip + 0x1b8be23]  ; -> 02064B64
004D8D41  ucomiss  xmm11, xmm1
004D8D45  jp       0x4d8d4e  ; -> 004D8D4E
004D8D47  mov      edx, 1
004D8D4C  je       0x4d8d50  ; -> 004D8D50
004D8D4E  mov      edx, esi
004D8D50  movss    xmm0, dword ptr [rip + 0x1b8be10]  ; -> 02064B68
004D8D58  ucomiss  xmm13, xmm0
004D8D5C  jp       0x4d8d65  ; -> 004D8D65
004D8D5E  mov      ecx, 1
004D8D63  je       0x4d8d67  ; -> 004D8D67
004D8D65  mov      ecx, esi
004D8D67  comiss   xmm2, xmm15
004D8D6B  mov      eax, esi
004D8D6D  mov      r9d, esi
004D8D70  seta     r9b
004D8D74  add      r9w, r9w
004D8D78  comiss   xmm1, xmm11
004D8D7C  seta     al
004D8D7F  add      r9w, ax
004D8D83  mov      eax, esi
004D8D85  add      r9w, r9w
004D8D89  comiss   xmm0, xmm13
004D8D8D  seta     al
004D8D90  add      r9w, ax
004D8D94  shl      r9w, 2
004D8D99  add      r9w, r8w
004D8D9D  add      r9w, r9w
004D8DA1  add      r9w, dx
004D8DA5  add      r9w, r9w
004D8DA9  add      r9w, cx
004D8DAD  add      r9w, r9w
004D8DB1  ucomiss  xmm2, xmm9
004D8DB5  mov      word ptr [rip + 0x1b8bd57], r9w  ; -> 02064B14
004D8DBD  jp       0x4d8dc6  ; -> 004D8DC6
004D8DBF  jne      0x4d8dc6  ; -> 004D8DC6
004D8DC1  mov      esi, 1
004D8DC6  ucomiss  xmm1, xmm10
004D8DCA  jp       0x4d8dd8  ; -> 004D8DD8
004D8DCC  jne      0x4d8dd8  ; -> 004D8DD8
004D8DCE  mov      edx, 1
004D8DD3  xor      r12d, r12d
004D8DD6  jmp      0x4d8dde  ; -> 004D8DDE
004D8DD8  xor      r12d, r12d
004D8DDB  mov      edx, r12d
004D8DDE  ucomiss  xmm0, xmm6
004D8DE1  jp       0x4d8dea  ; -> 004D8DEA
004D8DE3  mov      ecx, 1
004D8DE8  je       0x4d8ded  ; -> 004D8DED
004D8DEA  mov      ecx, r12d
004D8DED  comiss   xmm9, xmm2
004D8DF1  mov      eax, r12d
004D8DF4  mov      r8d, r12d
004D8DF7  seta     r8b
004D8DFB  add      r8w, r8w
004D8DFF  comiss   xmm10, xmm1
004D8E03  seta     al
004D8E06  add      r8w, ax
004D8E0A  mov      eax, r12d
004D8E0D  add      r8w, r8w
004D8E11  lea      r12, [rip + 0x1b8c018]  ; -> 02064E30
004D8E18  comiss   xmm6, xmm0
004D8E1B  movss    xmm6, dword ptr [rip + 0x1812e61]  ; -> 01CEBC84 [f32 16]
004D8E23  mulss    xmm0, xmm6
004D8E27  seta     al
004D8E2A  add      r8w, ax
004D8E2E  mulss    xmm5, xmm6
004D8E32  shl      r8w, 2
004D8E37  add      r8w, si
004D8E3B  mulss    xmm1, xmm6
004D8E3F  add      r8w, r8w
004D8E43  add      r8w, dx
004D8E47  mulss    xmm4, xmm6
004D8E4B  add      r8w, r8w
004D8E4F  add      r8w, cx
004D8E53  mulss    xmm3, xmm6
004D8E57  add      r8w, r8w
004D8E5B  mov      ecx, 0xe0
004D8E60  add      ecx, ebx
004D8E62  mulss    xmm2, xmm6
004D8E66  movzx    edx, cx
004D8E69  mov      word ptr [rip + 0x1b8bca5], r8w  ; -> 02064B16
004D8E71  cvttss2si eax, xmm5
004D8E75  and      dx, r11w
004D8E79  mov      dword ptr [rip + 0x1b8bcd1], eax  ; -> 02064B50
004D8E7F  cvttss2si eax, xmm4
004D8E83  mov      dword ptr [rip + 0x1b8bccb], eax  ; -> 02064B54
004D8E89  cvttss2si eax, xmm3
004D8E8D  mov      dword ptr [rip + 0x1b8bcc5], eax  ; -> 02064B58
004D8E93  cvttss2si eax, xmm2
004D8E97  mov      dword ptr [rip + 0x1b8bcc3], eax  ; -> 02064B60
004D8E9D  cvttss2si eax, xmm1
004D8EA1  movss    xmm1, dword ptr [rip + 0x1b8bf2b]  ; -> 02064DD4
004D8EA9  mov      dword ptr [rip + 0x1b8bcb5], eax  ; -> 02064B64
004D8EAF  cvttss2si eax, xmm0
004D8EB3  movaps   xmm0, xmm9
004D8EB7  mov      dword ptr [rip + 0x1b8bcab], eax  ; -> 02064B68
004D8EBD  movzx    eax, cx
004D8EC0  and      ax, r10w
004D8EC4  mulss    xmm0, xmm8
004D8EC9  mov      word ptr [rip + 0x1b8bf0c], ax  ; -> 02064DDC
004D8ED0  movzx    r10d, cx
004D8ED4  cwde     
004D8ED5  and      cx, r8w
004D8ED9  or       dx, ax
004D8EDC  mov      word ptr [rip + 0x1b8bf05], cx  ; -> 02064DE8
004D8EE3  movsx    eax, cx
004D8EE6  and      r10w, r9w
004D8EEA  or       r10w, ax
004D8EEE  movss    dword ptr [rip + 0x1b8bc66], xmm0  ; -> 02064B5C
004D8EF6  lea      eax, [rdi + 0x37e]
004D8EFC  movss    dword ptr [rip + 0x1b8bc68], xmm0  ; -> 02064B6C
004D8F04  movups   xmm0, xmmword ptr [rip + 0x1b8bc95]  ; -> 02064BA0
004D8F0B  shl      eax, 4
004D8F0E  movsxd   rcx, eax
004D8F11  mov      word ptr [rip + 0x1b8bec0], dx  ; -> 02064DD8
004D8F18  mov      word ptr [rip + 0x1b8bec0], r10w  ; -> 02064DE0
004D8F20  movups   xmmword ptr [rcx + r12], xmm0
004D8F25  cmp      dx, bx
004D8F28  je       0x4d8f4c  ; -> 004D8F4C
004D8F2A  comiss   xmm1, xmm7
004D8F2D  mov      word ptr [rip + 0x1b8bc27], r15w  ; -> 02064B5C
004D8F35  jb       0x4d8f42  ; -> 004D8F42
004D8F37  xor      esi, esi
004D8F39  mov      word ptr [rip + 0x1b8bc1e], si  ; -> 02064B5E
004D8F40  jmp      0x4d8f4e  ; -> 004D8F4E
004D8F42  or       dword ptr [rip + 0x1b8bc10], 0xffff0000  ; -> 02064B5C
004D8F4C  xor      esi, esi
004D8F4E  movups   xmm0, xmmword ptr [rip + 0x1b8bc5b]  ; -> 02064BB0
004D8F55  lea      eax, [rdi + 0x381]
004D8F5B  shl      eax, 4
004D8F5E  movsxd   rcx, eax
004D8F61  movups   xmmword ptr [rcx + r12], xmm0
004D8F66  cmp      r10w, bx
004D8F6A  je       0x4d8f8c  ; -> 004D8F8C
004D8F6C  comiss   xmm1, xmm7
004D8F6F  mov      word ptr [rip + 0x1b8bbf5], r15w  ; -> 02064B6C
004D8F77  jb       0x4d8f82  ; -> 004D8F82
004D8F79  mov      word ptr [rip + 0x1b8bbee], si  ; -> 02064B6E
004D8F80  jmp      0x4d8f8c  ; -> 004D8F8C
004D8F82  or       dword ptr [rip + 0x1b8bbe0], 0xffff0000  ; -> 02064B6C
004D8F8C  movups   xmm0, xmmword ptr [rip + 0x1b8bbbd]  ; -> 02064B50
004D8F93  lea      eax, [rdi + 0x380]
004D8F99  add      bp, 6
004D8F9D  movss    xmm6, dword ptr [rsp + 0x24]
004D8FA3  add      r13w, 2
004D8FA8  shl      eax, 4
004D8FAB  movsxd   rcx, eax
004D8FAE  lea      eax, [rdi + 0x383]
004D8FB4  shl      eax, 4
004D8FB7  mov      word ptr [rip + 0x1b8be26], bp  ; -> 02064DE4
004D8FBE  mov      word ptr [rip + 0x1b8bdfa], r13w  ; -> 02064DC0
004D8FC6  movups   xmmword ptr [rcx + r12], xmm0
004D8FCB  movsxd   rcx, eax
004D8FCE  movups   xmm0, xmmword ptr [rip + 0x1b8bb8b]  ; -> 02064B60
004D8FD5  movups   xmmword ptr [rcx + r12], xmm0
004D8FDA  test     r14w, r14w
004D8FDE  jg       0x4d80e0  ; -> 004D80E0
004D8FE4  lea      eax, [rbx + 1]
004D8FE7  and      r14w, ax
004D8FEB  mov      word ptr [rip + 0x1b8bdf6], ax  ; -> 02064DE8
004D8FF2  cmp      r14w, bx
004D8FF6  je       0x4d9004  ; -> 004D9004
004D8FF8  dec      r13w
004D8FFC  mov      word ptr [rip + 0x1b8bdbc], r13w  ; -> 02064DC0
004D9004  movzx    eax, word ptr [rip + 0x1b8bdb9]  ; -> 02064DC4
004D900B  lea      r14, [rip + 0x1b8be1e]  ; -> 02064E30
004D9012  movss    xmm3, dword ptr [rsp + 0x24]
004D9018  nop      dword ptr [rax + rax]
004D9020  movss    xmm0, dword ptr [rip + 0x1b8bbb8]  ; -> 02064BE0
004D9028  dec      ax
004D902B  addss    xmm0, dword ptr [rip + 0x1b8bbb1]  ; -> 02064BE4
004D9033  movzx    r12d, word ptr [rip + 0x1b8bd79]  ; -> 02064DB4
004D903B  movzx    ebp, bx
004D903E  mov      word ptr [rip + 0x1b8bd7f], ax  ; -> 02064DC4
004D9045  movsx    edx, bx
004D9048  mov      word ptr [rip + 0x1b8bd95], bx  ; -> 02064DE4
004D904F  movss    dword ptr [rip + 0x1b8bb89], xmm0  ; -> 02064BE0
004D9057  movss    xmm0, dword ptr [rip + 0x1b8bb91]  ; -> 02064BF0
004D905F  addss    xmm0, dword ptr [rip + 0x1b8bb91]  ; -> 02064BF8
004D9067  lea      eax, [rdx + 0x14]
004D906A  mov      word ptr [rip + 0x1b8bd4b], bx  ; -> 02064DBC
004D9071  shl      eax, 4
004D9074  movsxd   rcx, eax
004D9077  lea      eax, [rdx + 0x15]
004D907A  shl      eax, 4
004D907D  cdqe     
004D907F  movss    dword ptr [rip + 0x1b8bb69], xmm0  ; -> 02064BF0
004D9087  movzx    r9d, word ptr [rcx + r14 + 4]
004D908D  mov      rax, qword ptr [rax + r14 + 8]
004D9092  mov      qword ptr [rip + 0x1b8bb4f], rax  ; -> 02064BE8
004D9099  lea      eax, [rdx + 0x16]
004D909C  movss    xmm12, dword ptr [rip + 0x1b8bb43]  ; -> 02064BE8
004D90A5  shl      eax, 4
004D90A8  movsxd   rcx, eax
004D90AB  movss    xmm0, dword ptr [rcx + r14 + 0xc]
004D90B2  movss    xmm14, dword ptr [rcx + r14 + 4]
004D90B9  movss    dword ptr [rip + 0x1b8bb32], xmm14  ; -> 02064BF4
004D90C2  movss    dword ptr [rsp + 0x34], xmm0
004D90C8  movss    dword ptr [rip + 0x1b8bb2c], xmm0  ; -> 02064BFC
004D90D0  movss    xmm1, dword ptr [rip + 0x1b8bb08]  ; -> 02064BE0
004D90D8  movaps   xmm0, xmm12
004D90DC  addss    xmm12, dword ptr [rip + 0x1b8bb07]  ; -> 02064BEC
004D90E5  movsx    edx, r13w
004D90E9  movaps   xmm10, xmm3
004D90ED  mulss    xmm0, xmm8
004D90F2  movaps   xmm11, xmm3
004D90F6  movsx    r8d, r12w
004D90FA  mulss    xmm1, xmm8
004D90FF  movaps   xmm5, xmm9
004D9103  lea      eax, [rdx + 0x1e]
004D9106  shl      eax, 4
004D9109  addss    xmm5, xmm8
004D910E  movsxd   rcx, eax
004D9111  lea      eax, [rdx + 0x1f]
004D9114  shl      eax, 4
004D9117  movsx    edx, bp
004D911A  movss    dword ptr [rip + 0x1b8bb86], xmm0  ; -> 02064CA8
004D9122  movaps   xmm0, xmm12
004D9126  movups   xmm15, xmmword ptr [rcx + r14]
004D912B  movsxd   rcx, eax
004D912E  addss    xmm12, dword ptr [rip + 0x1b8bab5]  ; -> 02064BEC
004D9137  lea      eax, [rdx + 0x383]
004D913D  mulss    xmm10, xmm15
004D9142  shl      eax, 4
004D9145  movups   xmm6, xmmword ptr [rcx + r14]
004D914A  movsxd   rcx, eax
004D914D  lea      eax, [rdx + 0x37f]
004D9153  shl      eax, 4
004D9156  mulss    xmm11, xmm6
004D915B  movups   xmm2, xmmword ptr [rcx + r14]
004D9160  movsxd   rcx, eax
004D9163  lea      eax, [rdx + 0x382]
004D9169  shl      eax, 4
004D916C  mulss    xmm0, xmm8
004D9171  movups   xmm3, xmmword ptr [rcx + r14]
004D9176  movsxd   rcx, eax
004D9179  lea      eax, [rdx + 0x37e]
004D917F  shl      eax, 4
004D9182  movups   xmmword ptr [rip + 0x1b8ba86], xmm15  ; -> 02064C10
004D918A  movups   xmm4, xmmword ptr [rcx + r14]
004D918F  movsxd   rcx, eax
004D9192  lea      eax, [rdx + 0x381]
004D9198  mulss    xmm15, dword ptr [rip + 0x1b8ba2f]  ; -> 02064BD0
004D91A1  shl      eax, 4
004D91A4  movups   xmmword ptr [rip + 0x1b8b995], xmm6  ; -> 02064B40
004D91AB  movups   xmm13, xmmword ptr [rcx + r14]
004D91B0  movsxd   rcx, eax
004D91B3  lea      eax, [rdx + 0x380]
004D91B9  mulss    xmm6, dword ptr [rip + 0x1b8ba0f]  ; -> 02064BD0
004D91C1  addss    xmm15, xmm5
004D91C6  shl      eax, 4
004D91C9  movsxd   rdx, eax
004D91CC  lea      eax, [r8 + 2]
004D91D0  shl      eax, 4
004D91D3  movss    dword ptr [rsp + 0x30], xmm12
004D91DA  addss    xmm6, xmm5
004D91DE  movss    dword ptr [rip + 0x1b8ba01], xmm12  ; -> 02064BE8
004D91E7  movups   xmm12, xmmword ptr [rcx + r14]
004D91EC  movsxd   rcx, eax
004D91EF  lea      eax, [r8 + 8]
004D91F3  shl      eax, 4
004D91F6  movss    dword ptr [rip + 0x1b8baba], xmm0  ; -> 02064CB8
004D91FE  movups   xmm0, xmmword ptr [rdx + r14]
004D9203  mov      edx, r8d
004D9206  movss    dword ptr [rip + 0x1b8ba92], xmm1  ; -> 02064CA0
004D920E  movups   xmmword ptr [rcx + r14], xmm0
004D9213  movsxd   rcx, eax
004D9216  shl      edx, 4
004D9219  movss    dword ptr [rip + 0x1b8ba82], xmm10  ; -> 02064CA4
004D9222  movss    dword ptr [rip + 0x1b8ba82], xmm5  ; -> 02064CAC
004D922A  movups   xmmword ptr [rcx + r14], xmm2
004D922F  lea      eax, [rdx + 0x10]
004D9232  movss    dword ptr [rip + 0x1b8ba79], xmm11  ; -> 02064CB4
004D923B  movsxd   rcx, eax
004D923E  movss    dword ptr [rip + 0x1b8ba76], xmm5  ; -> 02064CBC
004D9246  movss    dword ptr [rip + 0x1b8ba62], xmm1  ; -> 02064CB0
004D924E  movups   xmmword ptr [rip + 0x1b8b91b], xmm3  ; -> 02064B70
004D9255  movups   xmmword ptr [rip + 0x1b8b924], xmm4  ; -> 02064B80
004D925C  movups   xmmword ptr [rsp + 0x70], xmm13
004D9262  movups   xmmword ptr [rsp + 0x80], xmm12
004D926B  minss    xmm6, dword ptr [rip + 0x1b8b965]  ; -> 02064BD8
004D9273  minss    xmm15, dword ptr [rip + 0x1b8b95c]  ; -> 02064BD8
004D927C  movups   xmm0, xmmword ptr [rip + 0x1b8ba1d]  ; -> 02064CA0
004D9283  lea      eax, [r8 + 7]
004D9287  add      r9w, -2
004D928C  movups   xmm1, xmmword ptr [rip + 0x1b8ba1d]  ; -> 02064CB0
004D9293  shl      eax, 4
004D9296  maxss    xmm6, dword ptr [rip + 0x1b8b93e]  ; -> 02064BDC
004D929E  maxss    xmm15, dword ptr [rip + 0x1b8b935]  ; -> 02064BDC
004D92A7  movups   xmmword ptr [rcx + r14], xmm3
004D92AC  movsxd   rcx, eax
004D92AF  movsxd   rax, edx
004D92B2  movaps   xmm3, xmm8
004D92B6  shufps   xmm3, xmm3, 0
004D92BA  movaps   xmm2, xmm3
004D92BD  movss    dword ptr [rip + 0x1b8b87b], xmm6  ; -> 02064B40
004D92C5  mulps    xmm2, xmm0
004D92C8  mov      word ptr [rsp + 0x190], r9w
004D92D1  movss    xmm0, dword ptr [rip + 0x1b8b8f3]  ; -> 02064BCC
004D92D9  movss    dword ptr [rip + 0x1b8b89b], xmm0  ; -> 02064B7C
004D92E1  movss    dword ptr [rip + 0x1b8b8a3], xmm0  ; -> 02064B8C
004D92E9  movups   xmm0, xmmword ptr [rsp + 0x50]
004D92EE  mov      word ptr [rip + 0x1b8bad2], r9w  ; -> 02064DC8
004D92F6  mulps    xmm3, xmm1
004D92F9  movss    xmm1, dword ptr [rip + 0x1b8b8d3]  ; -> 02064BD4
004D9301  movups   xmmword ptr [rcx + r14], xmm4
004D9306  movups   xmmword ptr [rax + r14], xmm13
004D930B  lea      eax, [r8 + 6]
004D930F  movaps   xmm13, xmm0
004D9313  movss    dword ptr [rip + 0x1b8b8f4], xmm15  ; -> 02064C10
004D931C  movups   xmmword ptr [rip + 0x1b8b82d], xmm2  ; -> 02064B50
004D9323  shl      eax, 4
004D9326  cmp      word ptr [rip + 0x1b8baa3], bx  ; -> 02064DD0
004D932D  movups   xmmword ptr [rip + 0x1b8b82c], xmm3  ; -> 02064B60
004D9334  movsxd   rcx, eax
004D9337  shufps   xmm3, xmm3, 0x55
004D933B  maxss    xmm0, xmm3
004D933F  shufps   xmm2, xmm2, 0x55
004D9343  maxss    xmm13, xmm2
004D9348  movups   xmmword ptr [rcx + r14], xmm12
004D934D  movss    xmm12, dword ptr [rip + 0x1b8b802]  ; -> 02064B58
004D9356  movss    dword ptr [rsp + 0x3c], xmm0
004D935C  movss    xmm0, dword ptr [rip + 0x1b8b8b4]  ; -> 02064C18
004D9364  mulss    xmm0, xmm1
004D9368  movss    dword ptr [rip + 0x1b8b8a8], xmm0  ; -> 02064C18
004D9370  movss    xmm0, dword ptr [rip + 0x1b8b8a4]  ; -> 02064C1C
004D9378  mulss    xmm0, xmm1
004D937C  movss    dword ptr [rip + 0x1b8b898], xmm0  ; -> 02064C1C
004D9384  movss    xmm0, dword ptr [rip + 0x1b8b7bc]  ; -> 02064B48
004D938C  mulss    xmm0, xmm1
004D9390  movss    dword ptr [rip + 0x1b8b7b0], xmm0  ; -> 02064B48
004D9398  movss    xmm0, dword ptr [rip + 0x1b8b7ac]  ; -> 02064B4C
004D93A0  mulss    xmm0, xmm1
004D93A4  movaps   xmm1, xmm15
004D93A8  mulss    xmm1, dword ptr [rip + 0x1b8b814]  ; -> 02064BC4
004D93B0  movss    dword ptr [rip + 0x1b8b794], xmm0  ; -> 02064B4C
004D93B8  movaps   xmm0, xmm15
004D93BC  mulss    xmm0, dword ptr [rip + 0x1b8b7fc]  ; -> 02064BC0
004D93C4  mulss    xmm15, dword ptr [rip + 0x1b8b7fb]  ; -> 02064BC8
004D93CD  movss    dword ptr [rsp + 0x44], xmm0
004D93D3  movaps   xmm0, xmm6
004D93D6  mulss    xmm0, dword ptr [rip + 0x1b8b7e2]  ; -> 02064BC0
004D93DE  movss    dword ptr [rsp + 0x40], xmm1
004D93E4  movss    dword ptr [rsp + 0x2c], xmm0
004D93EA  movaps   xmm0, xmm6
004D93ED  mulss    xmm0, dword ptr [rip + 0x1b8b7cf]  ; -> 02064BC4
004D93F5  mulss    xmm6, dword ptr [rip + 0x1b8b7cb]  ; -> 02064BC8
004D93FD  movss    dword ptr [rsp + 0x28], xmm0
004D9403  movss    xmm0, dword ptr [rip + 0x1b8b745]  ; -> 02064B50
004D940B  movups   xmmword ptr [rsp + 0x60], xmm6
004D9410  je       0x4d9686  ; -> 004D9686
004D9416  movss    xmm2, dword ptr [rip + 0x1b8b82a]  ; -> 02064C48
004D941E  movaps   xmm6, xmm0
004D9421  movss    xmm0, dword ptr [rip + 0x1b8b737]  ; -> 02064B60
004D9429  addss    xmm6, xmm9
004D942E  movaps   xmm1, xmm2
004D9431  mulss    xmm10, xmm10
004D9436  mulss    xmm2, dword ptr [rip + 0x1b8b72a]  ; -> 02064B68
004D943E  addss    xmm0, xmm9
004D9443  mulss    xmm1, xmm12
004D9448  movss    dword ptr [rip + 0x1b8b868], xmm2  ; -> 02064CB8
004D9450  mulss    xmm0, xmm0
004D9454  mulss    xmm2, xmm2
004D9458  movss    dword ptr [rip + 0x1b8b830], xmm0  ; -> 02064C90
004D9460  mulss    xmm0, xmm8
004D9465  movss    dword ptr [rip + 0x1b8b82b], xmm2  ; -> 02064C98
004D946D  mulss    xmm2, xmm8
004D9472  movss    dword ptr [rip + 0x1b8b82e], xmm1  ; -> 02064CA8
004D947A  mulss    xmm6, xmm6
004D947E  addss    xmm2, xmm0
004D9482  mulss    xmm1, xmm1
004D9486  movss    dword ptr [rip + 0x1b8b7f2], xmm6  ; -> 02064C80
004D948E  mulss    xmm6, xmm8
004D9493  cvtps2pd xmm0, xmm2
004D9496  movss    dword ptr [rip + 0x1b8b7ea], xmm1  ; -> 02064C88
004D949E  andps    xmm0, xmmword ptr [rip + 0x18128db]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004D94A5  mulss    xmm1, xmm8
004D94AA  cvtpd2ps xmm0, xmm0
004D94AE  addss    xmm6, xmm1
004D94B2  mulss    xmm11, xmm11
004D94B7  movss    dword ptr [rip + 0x1b8b7c4], xmm10  ; -> 02064C84
004D94C0  movss    dword ptr [rip + 0x1b8b7d4], xmm2  ; -> 02064C9C
004D94C8  movss    dword ptr [rip + 0x1b8b7c3], xmm11  ; -> 02064C94
004D94D1  movss    dword ptr [rip + 0x1b8b7b3], xmm6  ; -> 02064C8C
004D94D9  call     0x861f14  ; -> 00861F14 fn
004D94DE  cvtps2pd xmm1, xmm6
004D94E1  movaps   xmm10, xmm0
004D94E5  andps    xmm1, xmmword ptr [rip + 0x1812894]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
004D94EC  cvtpd2ps xmm0, xmm1
004D94F0  call     0x861f14  ; -> 00861F14 fn
004D94F5  movss    xmm3, dword ptr [rip + 0x1b8b73f]  ; -> 02064C3C
004D94FD  movaps   xmm1, xmm0
004D9500  addss    xmm1, xmm9
004D9505  mulss    xmm1, dword ptr [rip + 0x1b8b73f]  ; -> 02064C4C
004D950D  ucomiss  xmm3, xmm1
004D9510  jp       0x4d9519  ; -> 004D9519
004D9512  mov      eax, 1
004D9517  je       0x4d951b  ; -> 004D951B
004D9519  mov      eax, esi
004D951B  movss    xmm4, dword ptr [rip + 0x1b8b711]  ; -> 02064C34
004D9523  lea      edx, [rbx + 0x10]
004D9526  movss    xmm5, dword ptr [rip + 0x1b8b702]  ; -> 02064C30
004D952E  mov      ecx, esi
004D9530  movss    xmm6, dword ptr [rsp + 0x198]
004D9539  comiss   xmm1, xmm3
004D953C  seta     cl
004D953F  shl      cx, 4
004D9543  add      cx, ax
004D9546  movzx    eax, dx
004D9549  and      ax, cx
004D954C  cmp      ax, bx
004D954F  jne      0x4d9570  ; -> 004D9570
004D9551  mulss    xmm1, dword ptr [rsp + 0x20]
004D9557  movaps   xmm0, xmm4
004D955A  subss    xmm0, xmm5
004D955E  movss    dword ptr [rip + 0x1b8b73e], xmm0  ; -> 02064CA4
004D9566  mulss    xmm0, xmm1
004D956A  addss    xmm0, xmm5
004D956E  jmp      0x4d9594  ; -> 004D9594
004D9570  movss    xmm0, dword ptr [rip + 0x1b8b6c0]  ; -> 02064C38
004D9578  subss    xmm1, xmm3
004D957C  subss    xmm0, xmm4
004D9580  mulss    xmm1, xmm6
004D9584  movss    dword ptr [rip + 0x1b8b71c], xmm0  ; -> 02064CA8
004D958C  mulss    xmm0, xmm1
004D9590  addss    xmm0, xmm4
004D9594  movss    dword ptr [rip + 0x1b8b704], xmm0  ; -> 02064CA0
004D959C  movss    xmm11, dword ptr [rip + 0x1b8b627]  ; -> 02064BCC
004D95A5  movaps   xmm1, xmm9
004D95A9  addss    xmm1, xmm10
004D95AE  movaps   xmm2, xmm11
004D95B2  mulss    xmm2, xmm0
004D95B6  mulss    xmm1, dword ptr [rip + 0x1b8b68e]  ; -> 02064C4C
004D95BE  ucomiss  xmm3, xmm1
004D95C1  jp       0x4d95ca  ; -> 004D95CA
004D95C3  mov      ecx, 1
004D95C8  je       0x4d95cc  ; -> 004D95CC
004D95CA  mov      ecx, esi
004D95CC  comiss   xmm1, xmm3
004D95CF  mov      eax, esi
004D95D1  seta     al
004D95D4  shl      ax, 4
004D95D8  add      ax, cx
004D95DB  and      dx, ax
004D95DE  mov      word ptr [rip + 0x1b8b52b], ax  ; -> 02064B10
004D95E5  mov      word ptr [rip + 0x1b8b7fc], dx  ; -> 02064DE8
004D95EC  cmp      dx, bx
004D95EF  jne      0x4d9610  ; -> 004D9610
004D95F1  mulss    xmm1, dword ptr [rsp + 0x20]
004D95F7  movaps   xmm0, xmm4
004D95FA  subss    xmm0, xmm5
004D95FE  movss    dword ptr [rip + 0x1b8b6ae], xmm0  ; -> 02064CB4
004D9606  mulss    xmm0, xmm1
004D960A  addss    xmm0, xmm5
004D960E  jmp      0x4d9634  ; -> 004D9634
004D9610  movss    xmm0, dword ptr [rip + 0x1b8b620]  ; -> 02064C38
004D9618  subss    xmm1, xmm3
004D961C  subss    xmm0, xmm4
004D9620  mulss    xmm1, xmm6
004D9624  movss    dword ptr [rip + 0x1b8b68c], xmm0  ; -> 02064CB8
004D962C  mulss    xmm0, xmm1
004D9630  addss    xmm0, xmm4
004D9634  movss    dword ptr [rip + 0x1b8b674], xmm0  ; -> 02064CB0
004D963C  movss    xmm3, dword ptr [rip + 0x1b8b4c0]  ; -> 02064B04
004D9644  movaps   xmm1, xmm11
004D9648  comiss   xmm3, xmm2
004D964B  mulss    xmm1, xmm0
004D964F  ja       0x4d9654  ; -> 004D9654
004D9651  movaps   xmm2, xmm3
004D9654  movss    xmm0, dword ptr [rip + 0x1b8b4a8]  ; -> 02064B04
004D965C  comiss   xmm0, xmm1
004D965F  ja       0x4d9664  ; -> 004D9664
004D9661  movaps   xmm1, xmm0
004D9664  movss    xmm0, dword ptr [rip + 0x1b8b4e4]  ; -> 02064B50
004D966C  maxss    xmm2, xmm9
004D9671  maxss    xmm1, xmm9
004D9676  movss    dword ptr [rip + 0x1b8b4fe], xmm2  ; -> 02064B7C
004D967E  movss    dword ptr [rip + 0x1b8b506], xmm1  ; -> 02064B8C
004D9686  movss    xmm2, dword ptr [rip + 0x1b8b4ce]  ; -> 02064B5C
004D968E  movaps   xmm6, xmm0
004D9691  movups   xmm0, xmmword ptr [rip + 0x1b8b648]  ; -> 02064CE0
004D9698  movss    xmm1, dword ptr [rip + 0x1b8b658]  ; -> 02064CF8
004D96A0  mulss    xmm1, xmm13
004D96A5  shufps   xmm6, xmm6, 0
004D96A9  mulps    xmm6, xmm0
004D96AC  movss    xmm0, dword ptr [rip + 0x1b8b63c]  ; -> 02064CF0
004D96B4  mulss    xmm0, xmm13
004D96B9  movups   xmmword ptr [rip + 0x1b8b460], xmm6  ; -> 02064B20
004D96C0  movss    xmm3, dword ptr [rip + 0x1b8b45c]  ; -> 02064B24
004D96C8  addss    xmm6, xmm0
004D96CC  movss    xmm0, dword ptr [rip + 0x1b8b620]  ; -> 02064CF4
004D96D4  movss    xmm5, dword ptr [rip + 0x1b8b450]  ; -> 02064B2C
004D96DC  movss    xmm4, dword ptr [rip + 0x1b8b444]  ; -> 02064B28
004D96E4  mulss    xmm0, xmm13
004D96E9  addss    xmm4, xmm1
004D96ED  movss    xmm1, dword ptr [rip + 0x1b8b60f]  ; -> 02064D04
004D96F5  mulss    xmm1, xmm12
004D96FA  addss    xmm3, xmm0
004D96FE  movss    xmm0, dword ptr [rip + 0x1b8b5f6]  ; -> 02064CFC
004D9706  mulss    xmm0, xmm13
004D970B  addss    xmm5, xmm0
004D970F  movss    xmm0, dword ptr [rip + 0x1b8b5e9]  ; -> 02064D00
004D9717  mulss    xmm0, xmm12
004D971C  addss    xmm3, xmm1
004D9720  movss    xmm1, dword ptr [rip + 0x1b8b5e4]  ; -> 02064D0C
004D9728  mulss    xmm1, xmm12
004D972D  addss    xmm6, xmm0
004D9731  movss    xmm0, dword ptr [rip + 0x1b8b5cf]  ; -> 02064D08
004D9739  mulss    xmm0, xmm12
004D973E  addss    xmm5, xmm1
004D9742  movss    xmm1, dword ptr [rip + 0x1b8b5ce]  ; -> 02064D18
004D974A  mulss    xmm1, xmm2
004D974E  addss    xmm4, xmm0
004D9752  movss    xmm0, dword ptr [rip + 0x1b8b5b6]  ; -> 02064D10
004D975A  mulss    xmm0, xmm2
004D975E  addss    xmm0, xmm6
004D9762  addss    xmm1, xmm4
004D9766  movss    dword ptr [rip + 0x1b8b3e2], xmm0  ; -> 02064B50
004D976E  movss    xmm0, dword ptr [rip + 0x1b8b59e]  ; -> 02064D14
004D9776  mulss    xmm0, xmm2
004D977A  movss    dword ptr [rip + 0x1b8b3d6], xmm1  ; -> 02064B58
004D9782  addss    xmm0, xmm3
004D9786  movss    dword ptr [rip + 0x1b8b3c6], xmm0  ; -> 02064B54
004D978E  movss    xmm0, dword ptr [rip + 0x1b8b586]  ; -> 02064D1C
004D9796  mulss    xmm0, xmm2
004D979A  addss    xmm0, xmm5
004D979E  ucomiss  xmm0, xmm7
004D97A1  movss    dword ptr [rip + 0x1b8b3b3], xmm0  ; -> 02064B5C
004D97A9  jp       0x4d97b8  ; -> 004D97B8
004D97AB  jne      0x4d97b8  ; -> 004D97B8
004D97AD  movss    xmm10, dword ptr [rip + 0x426baa]  ; -> 00900360 [u32 0x7F7FFFFF]
004D97B6  jmp      0x4d97c1  ; -> 004D97C1
004D97B8  movaps   xmm10, xmm8
004D97BC  divss    xmm10, xmm0
004D97C1  movss    xmm2, dword ptr [rip + 0x1b8b43f]  ; -> 02064C08
004D97C9  movss    xmm0, dword ptr [rsp + 0x2c]
004D97CF  minss    xmm15, xmm2
004D97D4  movss    xmm1, dword ptr [rsp + 0x28]
004D97DA  minss    xmm0, xmm2
004D97DE  movss    xmm6, dword ptr [rip + 0x1b8b37a]  ; -> 02064B60
004D97E6  minss    xmm1, xmm2
004D97EA  movups   xmm11, xmmword ptr [rsp + 0x60]
004D97F0  movss    xmm12, dword ptr [rsp + 0x44]
004D97F7  movss    xmm13, dword ptr [rsp + 0x40]
004D97FE  minss    xmm12, xmm2
004D9803  movss    dword ptr [rsp + 0x2c], xmm0
004D9809  minss    xmm13, xmm2
004D980E  movups   xmm0, xmmword ptr [rip + 0x1b8b4cb]  ; -> 02064CE0
004D9815  movss    dword ptr [rsp + 0x28], xmm1
004D981B  minss    xmm11, xmm2
004D9820  movss    xmm2, dword ptr [rsp + 0x3c]
004D9826  movss    xmm1, dword ptr [rip + 0x1b8b4ca]  ; -> 02064CF8
004D982E  mulss    xmm1, xmm2
004D9832  shufps   xmm6, xmm6, 0
004D9836  mulps    xmm6, xmm0
004D9839  movss    xmm0, dword ptr [rip + 0x1b8b4af]  ; -> 02064CF0
004D9841  mulss    xmm0, xmm2
004D9845  movups   xmmword ptr [rip + 0x1b8b2d4], xmm6  ; -> 02064B20
004D984C  movss    xmm3, dword ptr [rip + 0x1b8b2d0]  ; -> 02064B24
004D9854  addss    xmm6, xmm0
004D9858  movss    xmm0, dword ptr [rip + 0x1b8b494]  ; -> 02064CF4
004D9860  movss    xmm5, dword ptr [rip + 0x1b8b2c4]  ; -> 02064B2C
004D9868  movss    xmm4, dword ptr [rip + 0x1b8b2b8]  ; -> 02064B28
004D9870  mulss    xmm0, xmm2
004D9874  addss    xmm4, xmm1
004D9878  movss    xmm1, dword ptr [rip + 0x1b8b484]  ; -> 02064D04
004D9880  addss    xmm3, xmm0
004D9884  movss    xmm0, dword ptr [rip + 0x1b8b470]  ; -> 02064CFC
004D988C  mulss    xmm0, xmm2
004D9890  movss    xmm2, dword ptr [rip + 0x1b8b2d0]  ; -> 02064B68
004D9898  mulss    xmm1, xmm2
004D989C  addss    xmm5, xmm0
004D98A0  movss    xmm0, dword ptr [rip + 0x1b8b458]  ; -> 02064D00
004D98A8  mulss    xmm0, xmm2
004D98AC  addss    xmm3, xmm1
004D98B0  movss    xmm1, dword ptr [rip + 0x1b8b454]  ; -> 02064D0C
004D98B8  mulss    xmm1, xmm2
004D98BC  addss    xmm6, xmm0
004D98C0  movss    xmm0, dword ptr [rip + 0x1b8b440]  ; -> 02064D08
004D98C8  mulss    xmm0, xmm2
004D98CC  movss    xmm2, dword ptr [rip + 0x1b8b298]  ; -> 02064B6C
004D98D4  addss    xmm5, xmm1
004D98D8  movss    xmm1, dword ptr [rip + 0x1b8b438]  ; -> 02064D18
004D98E0  addss    xmm4, xmm0
004D98E4  movss    dword ptr [rip + 0x1b8b238], xmm3  ; -> 02064B24
004D98EC  movss    xmm0, dword ptr [rip + 0x1b8b41c]  ; -> 02064D10
004D98F4  mulss    xmm0, xmm2
004D98F8  mulss    xmm1, xmm2
004D98FC  addss    xmm0, xmm6
004D9900  movss    dword ptr [rip + 0x1b8b218], xmm6  ; -> 02064B20
004D9908  movss    dword ptr [rip + 0x1b8b218], xmm4  ; -> 02064B28
004D9910  addss    xmm1, xmm4
004D9914  movss    dword ptr [rip + 0x1b8b210], xmm5  ; -> 02064B2C
004D991C  movss    dword ptr [rip + 0x1b8b23c], xmm0  ; -> 02064B60
004D9924  movss    xmm0, dword ptr [rip + 0x1b8b3e8]  ; -> 02064D14
004D992C  mulss    xmm0, xmm2
004D9930  movss    dword ptr [rip + 0x1b8b230], xmm1  ; -> 02064B68
004D9938  movss    xmm1, dword ptr [rip + 0x1b8b2cc]  ; -> 02064C0C
004D9940  addss    xmm0, xmm3
004D9944  movss    xmm3, dword ptr [rip + 0x1b8b3d0]  ; -> 02064D1C
004D994C  mulss    xmm3, xmm2
004D9950  maxss    xmm12, xmm1
004D9955  maxss    xmm13, xmm1
004D995A  maxss    xmm15, xmm1
004D995F  movss    dword ptr [rip + 0x1b8b1fd], xmm0  ; -> 02064B64
004D9967  addss    xmm3, xmm5
004D996B  movss    xmm0, dword ptr [rsp + 0x2c]
004D9971  maxss    xmm0, xmm1
004D9975  movss    dword ptr [rip + 0x1b8b1f2], xmm12  ; -> 02064B70
004D997E  movss    dword ptr [rip + 0x1b8b1ed], xmm13  ; -> 02064B74
004D9987  movss    dword ptr [rip + 0x1b8b1e8], xmm15  ; -> 02064B78
004D9990  movss    dword ptr [rip + 0x1b8b1d4], xmm3  ; -> 02064B6C
004D9998  movss    dword ptr [rip + 0x1b8b1e0], xmm0  ; -> 02064B80
004D99A0  movss    xmm0, dword ptr [rsp + 0x28]
004D99A6  maxss    xmm0, xmm1
004D99AA  ucomiss  xmm3, xmm7
004D99AD  maxss    xmm11, xmm1
004D99B2  movss    dword ptr [rip + 0x1b8b1ca], xmm0  ; -> 02064B84
004D99BA  movups   xmm1, xmmword ptr [rip + 0x1b8b18f]  ; -> 02064B50
004D99C1  movaps   xmm0, xmm10
004D99C5  shufps   xmm0, xmm0, 0
004D99C9  mulps    xmm1, xmm0
004D99CC  movaps   xmm0, xmm10
004D99D0  shufps   xmm0, xmm0, 0
004D99D4  movss    dword ptr [rip + 0x1b8b1ab], xmm11  ; -> 02064B88
004D99DD  movups   xmmword ptr [rip + 0x1b8b16c], xmm1  ; -> 02064B50
004D99E4  movups   xmm1, xmmword ptr [rsp + 0x70]
004D99E9  mulps    xmm1, xmm0
004D99EC  movups   xmmword ptr [rip + 0x1b8b1ad], xmm1  ; -> 02064BA0
004D99F3  jp       0x4d9a01  ; -> 004D9A01
004D99F5  jne      0x4d9a01  ; -> 004D9A01
004D99F7  movss    xmm2, dword ptr [rip + 0x426961]  ; -> 00900360 [u32 0x7F7FFFFF]
004D99FF  jmp      0x4d9a09  ; -> 004D9A09
004D9A01  movaps   xmm2, xmm8
004D9A05  divss    xmm2, xmm3
004D9A09  cmp      word ptr [rip + 0x1b8b3bc], bx  ; -> 02064DCC
004D9A10  movups   xmm0, xmmword ptr [rip + 0x1b8b159]  ; -> 02064B70
004D9A17  movups   xmm1, xmmword ptr [rip + 0x1b8b142]  ; -> 02064B60
004D9A1E  cvttps2dq xmm5, xmm0
004D9A22  movups   xmm0, xmmword ptr [rip + 0x1b8b157]  ; -> 02064B80
004D9A29  movss    dword ptr [rip + 0x1b8b0cf], xmm2  ; -> 02064B00
004D9A31  cvttps2dq xmm6, xmm0
004D9A35  movaps   xmm0, xmm2
004D9A38  shufps   xmm0, xmm0, 0
004D9A3C  mulps    xmm1, xmm0
004D9A3F  movaps   xmm0, xmm2
004D9A42  shufps   xmm0, xmm0, 0
004D9A46  movups   xmmword ptr [rip + 0x1b8b123], xmm5  ; -> 02064B70
004D9A4D  movups   xmmword ptr [rip + 0x1b8b10c], xmm1  ; -> 02064B60
004D9A54  movups   xmm1, xmmword ptr [rsp + 0x80]
004D9A5C  movups   xmmword ptr [rip + 0x1b8b11d], xmm6  ; -> 02064B80
004D9A63  mulps    xmm1, xmm0
004D9A66  movups   xmmword ptr [rip + 0x1b8b143], xmm1  ; -> 02064BB0
004D9A6D  jne      0x4d9acf  ; -> 004D9ACF
004D9A6F  movss    xmm2, dword ptr [rip + 0x1b8b179]  ; -> 02064BF0
004D9A77  movaps   xmm3, xmm14
004D9A7B  addss    xmm14, dword ptr [rsp + 0x34]
004D9A82  movss    xmm11, dword ptr [rip + 0x1928dad]  ; -> 01E02838 [u32 0x00000000]
004D9A8B  movaps   xmm0, xmm11
004D9A8F  mulss    xmm2, xmm8
004D9A94  addss    xmm0, xmm8
004D9A99  mulss    xmm3, xmm8
004D9A9E  movaps   xmm1, xmm14
004D9AA2  movaps   xmm4, xmm2
004D9AA5  addss    xmm14, dword ptr [rsp + 0x34]
004D9AAC  mulss    xmm1, xmm8
004D9AB1  movss    dword ptr [rip + 0x1b8b0ef], xmm0  ; -> 02064BA8
004D9AB9  movss    dword ptr [rip + 0x1b8b0f7], xmm0  ; -> 02064BB8
004D9AC1  movss    dword ptr [rip + 0x1b8b12a], xmm14  ; -> 02064BF4
004D9ACA  jmp      0x4d9cb3  ; -> 004D9CB3
004D9ACF  movss    xmm1, dword ptr [rip + 0x1b8b079]  ; -> 02064B50
004D9AD7  subss    xmm1, dword ptr [rip + 0x1b8b1e1]  ; -> 02064CC0
004D9ADF  movss    xmm0, dword ptr [rip + 0x1b8b06d]  ; -> 02064B54
004D9AE7  subss    xmm0, dword ptr [rip + 0x1b8b1d5]  ; -> 02064CC4
004D9AEF  ucomiss  xmm1, xmm7
004D9AF2  movss    dword ptr [rip + 0x1b8b0a6], xmm1  ; -> 02064BA0
004D9AFA  movss    dword ptr [rip + 0x1b8b0a2], xmm0  ; -> 02064BA4
004D9B02  jp       0x4d9b06  ; -> 004D9B06
004D9B04  je       0x4d9b0d  ; -> 004D9B0D
004D9B06  ucomiss  xmm0, xmm7
004D9B09  jp       0x4d9b22  ; -> 004D9B22
004D9B0B  jne      0x4d9b22  ; -> 004D9B22
004D9B0D  call     0x22cc40  ; -> 0022CC40 fn
004D9B12  movss    xmm0, dword ptr [rip + 0x1b8b08a]  ; -> 02064BA4
004D9B1A  movss    xmm1, dword ptr [rip + 0x1b8b07e]  ; -> 02064BA0
004D9B22  comiss   xmm7, xmm1
004D9B25  ja       0x4d9b2c  ; -> 004D9B2C
004D9B27  comiss   xmm7, xmm0
004D9B2A  jbe      0x4d9b31  ; -> 004D9B31
004D9B2C  call     0x22cc30  ; -> 0022CC30 fn
004D9B31  call     0x22cc20  ; -> 0022CC20 fn
004D9B36  movss    xmm1, dword ptr [rip + 0x1b8b022]  ; -> 02064B60
004D9B3E  subss    xmm1, dword ptr [rip + 0x1b8b17a]  ; -> 02064CC0
004D9B46  movss    xmm0, dword ptr [rip + 0x1b8b016]  ; -> 02064B64
004D9B4E  subss    xmm0, dword ptr [rip + 0x1b8b16e]  ; -> 02064CC4
004D9B56  ucomiss  xmm1, xmm7
004D9B59  movss    dword ptr [rip + 0x1b8b04f], xmm1  ; -> 02064BB0
004D9B61  movss    dword ptr [rip + 0x1b8b04b], xmm0  ; -> 02064BB4
004D9B69  jp       0x4d9b6d  ; -> 004D9B6D
004D9B6B  je       0x4d9b74  ; -> 004D9B74
004D9B6D  ucomiss  xmm0, xmm7
004D9B70  jp       0x4d9b89  ; -> 004D9B89
004D9B72  jne      0x4d9b89  ; -> 004D9B89
004D9B74  call     0x22cc40  ; -> 0022CC40 fn
004D9B79  movss    xmm0, dword ptr [rip + 0x1b8b033]  ; -> 02064BB4
004D9B81  movss    xmm1, dword ptr [rip + 0x1b8b027]  ; -> 02064BB0
004D9B89  comiss   xmm7, xmm1
004D9B8C  ja       0x4d9b93  ; -> 004D9B93
004D9B8E  comiss   xmm7, xmm0
004D9B91  jbe      0x4d9b98  ; -> 004D9B98
004D9B93  call     0x22cc30  ; -> 0022CC30 fn
004D9B98  call     0x22cc20  ; -> 0022CC20 fn
004D9B9D  movss    xmm11, dword ptr [rip + 0x1928c92]  ; -> 01E02838 [u32 0x00000000]
004D9BA6  movss    xmm8, dword ptr [rip + 0x1928c8d]  ; -> 01E0283C [f32 1]
004D9BAF  movaps   xmm0, xmm11
004D9BB3  movss    xmm2, dword ptr [rip + 0x1b8afe5]  ; -> 02064BA0
004D9BBB  addss    xmm0, xmm8
004D9BC0  movss    xmm3, dword ptr [rip + 0x1b8afdc]  ; -> 02064BA4
004D9BC8  movss    xmm4, dword ptr [rip + 0x1b8afe0]  ; -> 02064BB0
004D9BD0  movss    xmm1, dword ptr [rip + 0x1b8afdc]  ; -> 02064BB4
004D9BD8  movzx    eax, word ptr [rip + 0x1b8b1e9]  ; -> 02064DC8
004D9BDF  mulss    xmm2, dword ptr [rip + 0x1b8b0e9]  ; -> 02064CD0
004D9BE7  movzx    ebx, word ptr [rip + 0x1b8af1e]  ; -> 02064B0C
004D9BEE  mulss    xmm3, dword ptr [rip + 0x1b8b0de]  ; -> 02064CD4
004D9BF6  movzx    r12d, word ptr [rip + 0x1b8b1b6]  ; -> 02064DB4
004D9BFE  mulss    xmm4, dword ptr [rip + 0x1b8b0ca]  ; -> 02064CD0
004D9C06  movzx    r13d, word ptr [rip + 0x1b8b1b2]  ; -> 02064DC0
004D9C0E  mulss    xmm1, dword ptr [rip + 0x1b8b0be]  ; -> 02064CD4
004D9C16  movzx    r15d, word ptr [rip + 0x1b8b1b6]  ; -> 02064DD4
004D9C1E  movss    xmm9, dword ptr [rip + 0x1928c09]  ; -> 01E02830 [u32 0x00000000]
004D9C27  movss    xmm14, dword ptr [rip + 0x1b8afc4]  ; -> 02064BF4
004D9C30  movups   xmm5, xmmword ptr [rip + 0x1b8af39]  ; -> 02064B70
004D9C37  movzx    ebp, word ptr [rip + 0x1b8b1a6]  ; -> 02064DE4
004D9C3E  movups   xmm6, xmmword ptr [rip + 0x1b8af3b]  ; -> 02064B80
004D9C45  mov      word ptr [rsp + 0x190], ax
004D9C4D  movss    dword ptr [rip + 0x1b8af53], xmm0  ; -> 02064BA8
004D9C55  movss    dword ptr [rip + 0x1b8af5b], xmm0  ; -> 02064BB8
004D9C5D  movss    xmm0, dword ptr [rip + 0x1b8afbf]  ; -> 02064C24
004D9C65  movups   xmmword ptr [rsp + 0x50], xmm0
004D9C6A  movss    xmm0, dword ptr [rip + 0x1b8afd2]  ; -> 02064C44
004D9C72  movss    dword ptr [rsp + 0x198], xmm0
004D9C7B  movss    xmm0, dword ptr [rip + 0x1b8afbd]  ; -> 02064C40
004D9C83  movss    dword ptr [rsp + 0x20], xmm0
004D9C89  movss    xmm0, dword ptr [rip + 0x1b8afc3]  ; -> 02064C54
004D9C91  movss    dword ptr [rsp + 0x24], xmm0
004D9C97  movss    xmm0, dword ptr [rip + 0x1b8af49]  ; -> 02064BE8
004D9C9F  movss    dword ptr [rsp + 0x30], xmm0
004D9CA5  movss    xmm0, dword ptr [rip + 0x1b8af4f]  ; -> 02064BFC
004D9CAD  movss    dword ptr [rsp + 0x34], xmm0
004D9CB3  addss    xmm2, dword ptr [rip + 0x1b8af5d]  ; -> 02064C18
004D9CBB  addss    xmm3, dword ptr [rip + 0x1b8af59]  ; -> 02064C1C
004D9CC3  addss    xmm4, dword ptr [rip + 0x1b8ae7d]  ; -> 02064B48
004D9CCB  addss    xmm1, dword ptr [rip + 0x1b8ae79]  ; -> 02064B4C
004D9CD3  movss    xmm10, dword ptr [rip + 0x1b8ae74]  ; -> 02064B50
004D9CDC  lea      rdx, [rip + 0x1b8b14d]  ; -> 02064E30
004D9CE3  movss    xmm13, dword ptr [rip + 0x1b8ae44]  ; -> 02064B30
004D9CEC  movsx    r14d, bp
004D9CF0  movsx    esi, r12w
004D9CF4  movss    dword ptr [rip + 0x1b8aea4], xmm2  ; -> 02064BA0
004D9CFC  movss    dword ptr [rip + 0x1b8aea0], xmm3  ; -> 02064BA4
004D9D04  lea      eax, [r14 + 0x37f]
004D9D0B  movss    dword ptr [rip + 0x1b8ae9d], xmm4  ; -> 02064BB0
004D9D13  shl      eax, 4
004D9D16  movsxd   rcx, eax
004D9D19  lea      eax, [r14 + 0x382]
004D9D20  shl      eax, 4
004D9D23  movss    dword ptr [rip + 0x1b8ae89], xmm1  ; -> 02064BB4
004D9D2B  movups   xmmword ptr [rcx + rdx], xmm5
004D9D2F  movsxd   rcx, eax
004D9D32  lea      eax, [rsi + 4]
004D9D35  shl      eax, 4
004D9D38  movups   xmmword ptr [rcx + rdx], xmm6
004D9D3C  movsxd   rcx, eax
004D9D3F  lea      eax, [rsi + 0xa]
004D9D42  shl      eax, 4
004D9D45  ucomiss  xmm13, xmm10
004D9D49  movups   xmmword ptr [rcx + rdx], xmm5
004D9D4D  movsxd   rcx, eax
004D9D50  movups   xmmword ptr [rcx + rdx], xmm6
004D9D54  jp       0x4d9d60  ; -> 004D9D60
004D9D56  jne      0x4d9d60  ; -> 004D9D60
004D9D58  xor      ebp, ebp
004D9D5A  lea      r8d, [rbp + 1]
004D9D5E  jmp      0x4d9d65  ; -> 004D9D65
004D9D60  xor      ebp, ebp
004D9D62  mov      r8d, ebp
004D9D65  movss    xmm6, dword ptr [rip + 0x1b8ade7]  ; -> 02064B54
004D9D6D  movss    xmm0, dword ptr [rip + 0x1b8adbf]  ; -> 02064B34
004D9D75  ucomiss  xmm0, xmm6
004D9D78  jp       0x4d9d81  ; -> 004D9D81
004D9D7A  mov      edx, 1
004D9D7F  je       0x4d9d83  ; -> 004D9D83
004D9D81  mov      edx, ebp
004D9D83  movss    xmm5, dword ptr [rip + 0x1b8adcd]  ; -> 02064B58
004D9D8B  movss    xmm12, dword ptr [rip + 0x1b8ada4]  ; -> 02064B38
004D9D94  ucomiss  xmm12, xmm5
004D9D98  jp       0x4d9da1  ; -> 004D9DA1
004D9D9A  mov      ecx, 1
004D9D9F  je       0x4d9da3  ; -> 004D9DA3
004D9DA1  mov      ecx, ebp
004D9DA3  comiss   xmm10, xmm13
004D9DA7  mov      eax, ebp
004D9DA9  mov      r10d, ebp
004D9DAC  mov      edi, 0xe0
004D9DB1  seta     r10b
004D9DB5  add      r10w, r10w
004D9DB9  comiss   xmm6, xmm0
004D9DBC  seta     al
004D9DBF  add      r10w, ax
004D9DC3  mov      eax, ebp
004D9DC5  add      r10w, r10w
004D9DC9  comiss   xmm5, xmm12
004D9DCD  seta     al
004D9DD0  add      edi, ebx
004D9DD2  add      r10w, ax
004D9DD6  shl      r10w, 2
004D9DDB  add      r10w, r8w
004D9DDF  add      r10w, r10w
004D9DE3  add      r10w, dx
004D9DE7  add      r10w, r10w
004D9DEB  add      r10w, cx
004D9DEF  add      r10w, r10w
004D9DF3  ucomiss  xmm10, xmm9
004D9DF7  mov      word ptr [rip + 0x1b8ad11], r10w  ; -> 02064B10
004D9DFF  jp       0x4d9e09  ; -> 004D9E09
004D9E01  mov      r9d, 1
004D9E07  je       0x4d9e0c  ; -> 004D9E0C
004D9E09  mov      r9d, ebp
004D9E0C  movss    xmm1, dword ptr [rip + 0x1928a20]  ; -> 01E02834 [u32 0x00000000]
004D9E14  ucomiss  xmm6, xmm1
004D9E17  jp       0x4d9e20  ; -> 004D9E20
004D9E19  mov      edx, 1
004D9E1E  je       0x4d9e22  ; -> 004D9E22
004D9E20  mov      edx, ebp
004D9E22  ucomiss  xmm5, xmm11
004D9E26  jp       0x4d9e2f  ; -> 004D9E2F
004D9E28  mov      ecx, 1
004D9E2D  je       0x4d9e31  ; -> 004D9E31
004D9E2F  mov      ecx, ebp
004D9E31  movss    xmm4, dword ptr [rip + 0x1b8ad27]  ; -> 02064B60
004D9E39  mov      eax, ebp
004D9E3B  comiss   xmm9, xmm10
004D9E3F  mov      r8d, ebp
004D9E42  seta     r8b
004D9E46  add      r8w, r8w
004D9E4A  comiss   xmm1, xmm6
004D9E4D  seta     al
004D9E50  add      r8w, ax
004D9E54  mov      eax, ebp
004D9E56  add      r8w, r8w
004D9E5A  comiss   xmm11, xmm5
004D9E5E  seta     al
004D9E61  add      r8w, ax
004D9E65  shl      r8w, 2
004D9E6A  add      r8w, r9w
004D9E6E  add      r8w, r8w
004D9E72  add      r8w, dx
004D9E76  add      r8w, r8w
004D9E7A  add      r8w, cx
004D9E7E  add      r8w, r8w
004D9E82  ucomiss  xmm13, xmm4
004D9E86  mov      word ptr [rip + 0x1b8ac84], r8w  ; -> 02064B12
004D9E8E  jp       0x4d9e98  ; -> 004D9E98
004D9E90  mov      r11d, 1
004D9E96  je       0x4d9e9b  ; -> 004D9E9B
004D9E98  mov      r11d, ebp
004D9E9B  movss    xmm3, dword ptr [rip + 0x1b8acc1]  ; -> 02064B64
004D9EA3  ucomiss  xmm0, xmm3
004D9EA6  jp       0x4d9eaf  ; -> 004D9EAF
004D9EA8  mov      edx, 1
004D9EAD  je       0x4d9eb1  ; -> 004D9EB1
004D9EAF  mov      edx, ebp
004D9EB1  movss    xmm2, dword ptr [rip + 0x1b8acaf]  ; -> 02064B68
004D9EB9  ucomiss  xmm12, xmm2
004D9EBD  jp       0x4d9ec6  ; -> 004D9EC6
004D9EBF  mov      ecx, 1
004D9EC4  je       0x4d9ec8  ; -> 004D9EC8
004D9EC6  mov      ecx, ebp
004D9EC8  comiss   xmm4, xmm13
004D9ECC  mov      eax, ebp
004D9ECE  mov      r9d, ebp
004D9ED1  seta     r9b
004D9ED5  add      r9w, r9w
004D9ED9  comiss   xmm3, xmm0
004D9EDC  seta     al
004D9EDF  add      r9w, ax
004D9EE3  mov      eax, ebp
004D9EE5  add      r9w, r9w
004D9EE9  comiss   xmm2, xmm12
004D9EED  movups   xmm12, xmmword ptr [rip + 0x1b8acab]  ; -> 02064BA0
004D9EF5  seta     al
004D9EF8  add      r9w, ax
004D9EFC  lea      eax, [r14 + 0x37e]
004D9F03  shl      r9w, 2
004D9F08  add      r9w, r11w
004D9F0C  shl      eax, 4
004D9F0F  add      r9w, r9w
004D9F13  add      r9w, dx
004D9F17  add      r9w, r9w
004D9F1B  add      r9w, cx
004D9F1F  movsxd   rcx, eax
004D9F22  add      r9w, r9w
004D9F26  lea      rax, [rip + 0x1b8af03]  ; -> 02064E30
004D9F2D  ucomiss  xmm4, xmm9
004D9F31  mov      word ptr [rip + 0x1b8abdb], r9w  ; -> 02064B14
004D9F39  movups   xmmword ptr [rcx + rax], xmm12
004D9F3E  jp       0x4d9f47  ; -> 004D9F47
004D9F40  jne      0x4d9f47  ; -> 004D9F47
004D9F42  mov      ebp, 1
004D9F47  ucomiss  xmm3, xmm1
004D9F4A  jp       0x4d9f56  ; -> 004D9F56
004D9F4C  jne      0x4d9f56  ; -> 004D9F56
004D9F4E  xor      eax, eax
004D9F50  lea      r11d, [rax + 1]
004D9F54  jmp      0x4d9f5b  ; -> 004D9F5B
004D9F56  xor      eax, eax
004D9F58  mov      r11d, eax
004D9F5B  ucomiss  xmm2, xmm11
004D9F5F  jp       0x4d9f68  ; -> 004D9F68
004D9F61  mov      ecx, 1
004D9F66  je       0x4d9f6a  ; -> 004D9F6A
004D9F68  mov      ecx, eax
004D9F6A  movss    xmm13, dword ptr [rip + 0x1811d11]  ; -> 01CEBC84 [f32 16]
004D9F73  mov      edx, eax
004D9F75  comiss   xmm9, xmm4
004D9F79  mulss    xmm10, xmm13
004D9F7E  seta     dl
004D9F81  mulss    xmm6, xmm13
004D9F86  add      dx, dx
004D9F89  mulss    xmm5, xmm13
004D9F8E  comiss   xmm1, xmm3
004D9F91  mulss    xmm4, xmm13
004D9F96  movaps   xmm1, xmm9
004D9F9A  seta     al
004D9F9D  mulss    xmm1, xmm8
004D9FA2  add      dx, ax
004D9FA5  xor      eax, eax
004D9FA7  add      dx, dx
004D9FAA  mulss    xmm3, xmm13
004D9FAF  comiss   xmm11, xmm2
004D9FB3  movups   xmm11, xmmword ptr [rip + 0x1b8abf5]  ; -> 02064BB0
004D9FBB  seta     al
004D9FBE  mulss    xmm2, xmm13
004D9FC3  add      dx, ax
004D9FC6  lea      eax, [r14 + 0x381]
004D9FCD  movss    dword ptr [rip + 0x1b8ab87], xmm1  ; -> 02064B5C
004D9FD5  shl      eax, 4
004D9FD8  shl      dx, 2
004D9FDC  add      dx, bp
004D9FDF  movss    dword ptr [rip + 0x1b8ab85], xmm1  ; -> 02064B6C
004D9FE7  movss    xmm1, dword ptr [rip + 0x1b8ade5]  ; -> 02064DD4
004D9FEF  lea      rbp, [rip + 0x1b8ae3a]  ; -> 02064E30
004D9FF6  add      dx, dx
004D9FF9  add      dx, r11w
004D9FFD  movzx    r11d, di
004DA001  add      dx, dx
004DA004  and      r11w, r10w
004DA008  add      dx, cx
004DA00B  movsxd   rcx, eax
004DA00E  cvttss2si eax, xmm10
004DA013  add      dx, dx
004DA016  mov      word ptr [rip + 0x1b8aaf9], dx  ; -> 02064B16
004DA01D  movups   xmmword ptr [rcx + rbp], xmm11
004DA022  mov      dword ptr [rip + 0x1b8ab28], eax  ; -> 02064B50
004DA028  movzx    ecx, di
004DA02B  and      cx, r8w
004DA02F  movzx    r8d, di
004DA033  cvttss2si eax, xmm6
004DA037  and      di, dx
004DA03A  and      r8w, r9w
004DA03E  mov      dword ptr [rip + 0x1b8ab10], eax  ; -> 02064B54
004DA044  cvttss2si eax, xmm5
004DA048  mov      dword ptr [rip + 0x1b8ab0a], eax  ; -> 02064B58
004DA04E  cvttss2si eax, xmm4
004DA052  mov      dword ptr [rip + 0x1b8ab08], eax  ; -> 02064B60
004DA058  cvttss2si eax, xmm3
004DA05C  mov      dword ptr [rip + 0x1b8ab02], eax  ; -> 02064B64
004DA062  cvttss2si eax, xmm2
004DA066  mov      dword ptr [rip + 0x1b8aafc], eax  ; -> 02064B68
004DA06C  movsx    eax, cx
004DA06F  or       r11w, ax
004DA073  movsx    eax, di
004DA076  or       r8w, ax
004DA07A  lea      eax, [rsi + 3]
004DA07D  shl      eax, 4
004DA080  movsxd   rcx, eax
004DA083  movups   xmmword ptr [rcx + rbp], xmm12
004DA088  cmp      r11w, bx
004DA08C  je       0x4da0b0  ; -> 004DA0B0
004DA08E  comiss   xmm1, xmm7
004DA091  mov      word ptr [rip + 0x1b8aac3], r15w  ; -> 02064B5C
004DA099  jb       0x4da0a6  ; -> 004DA0A6
004DA09B  xor      edx, edx
004DA09D  mov      word ptr [rip + 0x1b8aaba], dx  ; -> 02064B5E
004DA0A4  jmp      0x4da0b2  ; -> 004DA0B2
004DA0A6  or       dword ptr [rip + 0x1b8aaac], 0xffff0000  ; -> 02064B5C
004DA0B0  xor      edx, edx
004DA0B2  lea      eax, [rsi + 9]
004DA0B5  shl      eax, 4
004DA0B8  movsxd   rcx, eax
004DA0BB  movups   xmmword ptr [rcx + rbp], xmm11
004DA0C0  cmp      r8w, bx
004DA0C4  je       0x4da0e6  ; -> 004DA0E6
004DA0C6  comiss   xmm1, xmm7
004DA0C9  mov      word ptr [rip + 0x1b8aa9b], r15w  ; -> 02064B6C
004DA0D1  jb       0x4da0dc  ; -> 004DA0DC
004DA0D3  mov      word ptr [rip + 0x1b8aa94], dx  ; -> 02064B6E
004DA0DA  jmp      0x4da0e6  ; -> 004DA0E6
004DA0DC  or       dword ptr [rip + 0x1b8aa86], 0xffff0000  ; -> 02064B6C
004DA0E6  movups   xmm2, xmmword ptr [rip + 0x1b8aa63]  ; -> 02064B50
004DA0ED  lea      eax, [r14 + 0x380]
004DA0F4  movups   xmm1, xmmword ptr [rip + 0x1b8aa65]  ; -> 02064B60
004DA0FB  shl      eax, 4
004DA0FE  movsxd   rcx, eax
004DA101  lea      eax, [r14 + 0x383]
004DA108  shl      eax, 4
004DA10B  lea      r14, [rip + 0x1b8ad1e]  ; -> 02064E30
004DA112  movups   xmmword ptr [rcx + rbp], xmm2
004DA116  movzx    ebp, word ptr [rip + 0x1b8acc7]  ; -> 02064DE4
004DA11D  movsxd   rcx, eax
004DA120  add      bp, 6
004DA124  lea      eax, [rsi + 5]
004DA127  mov      word ptr [rip + 0x1b8acb6], bp  ; -> 02064DE4
004DA12E  shl      eax, 4
004DA131  movsxd   r9, eax
004DA134  lea      eax, [rsi + 0xb]
004DA137  shl      eax, 4
004DA13A  movsxd   rdi, eax
004DA13D  lea      eax, [rsi + 2]
004DA140  shl      eax, 4
004DA143  movsxd   r10, eax
004DA146  movups   xmmword ptr [rcx + r14], xmm1
004DA14B  movups   xmmword ptr [r9 + r14], xmm2
004DA150  movups   xmmword ptr [rdi + r14], xmm1
004DA155  movsx    eax, word ptr [r10 + r14 + 0xc]
004DA15B  mov      word ptr [rip + 0x1b8ac7a], ax  ; -> 02064DDC
004DA162  mov      edx, eax
004DA164  lea      eax, [rsi + 8]
004DA167  shl      eax, 4
004DA16A  movsxd   rsi, eax
004DA16D  movsx    eax, word ptr [rsi + r14 + 0xc]
004DA173  or       r8w, ax
004DA177  movsx    eax, word ptr [rip + 0x1b8ac3e]  ; -> 02064DBC
004DA17E  or       ax, dx
004DA181  movzx    ecx, r8w
004DA185  or       r11w, ax
004DA189  mov      word ptr [rip + 0x1b8ac58], cx  ; -> 02064DE8
004DA190  movsx    eax, r11w
004DA194  or       r8w, ax
004DA198  mov      word ptr [rip + 0x1b8ac38], r11w  ; -> 02064DD8
004DA1A0  mov      word ptr [rip + 0x1b8ac38], r8w  ; -> 02064DE0
004DA1A8  mov      word ptr [rip + 0x1b8ac0d], cx  ; -> 02064DBC
004DA1AF  cmp      r11w, bx
004DA1B3  je       0x4da1c3  ; -> 004DA1C3
004DA1B5  movzx    eax, r15w
004DA1B9  mov      dword ptr [r10 + r14 + 0xc], eax
004DA1BE  mov      dword ptr [r9 + r14 + 0xc], eax
004DA1C3  movzx    ecx, word ptr [rip + 0x1b8abee]  ; -> 02064DB8
004DA1CA  add      cx, 2
004DA1CE  mov      word ptr [rip + 0x1b8abe3], cx  ; -> 02064DB8
004DA1D5  cmp      r8w, bx
004DA1D9  je       0x4da1e9  ; -> 004DA1E9
004DA1DB  movzx    eax, r15w
004DA1DF  mov      dword ptr [rsi + r14 + 0xc], eax
004DA1E4  mov      dword ptr [rdi + r14 + 0xc], eax
004DA1E9  movzx    r9d, word ptr [rsp + 0x190]
004DA1F2  add      r12w, 0xc
004DA1F7  movss    xmm12, dword ptr [rsp + 0x30]
004DA1FE  add      r13w, 2
004DA203  movss    xmm3, dword ptr [rsp + 0x24]
004DA209  mov      esi, 0
004DA20E  mov      word ptr [rip + 0x1b8ab9e], r12w  ; -> 02064DB4
004DA216  mov      word ptr [rip + 0x1b8aba2], r13w  ; -> 02064DC0
004DA21E  test     r9w, r9w
004DA222  jg       0x4d90d0  ; -> 004D90D0
004DA228  lea      eax, [rbx + 1]
004DA22B  and      r9w, ax
004DA22F  mov      word ptr [rip + 0x1b8abb2], ax  ; -> 02064DE8
004DA236  mov      word ptr [rip + 0x1b8ab8a], r9w  ; -> 02064DC8
004DA23E  cmp      r9w, bx
004DA242  je       0x4da267  ; -> 004DA267
004DA244  dec      r13w
004DA248  add      r12w, 6
004DA24D  dec      cx
004DA250  mov      word ptr [rip + 0x1b8ab68], r13w  ; -> 02064DC0
004DA258  mov      word ptr [rip + 0x1b8ab59], cx  ; -> 02064DB8
004DA25F  mov      word ptr [rip + 0x1b8ab4d], r12w  ; -> 02064DB4
004DA267  movsx    edx, word ptr [rip + 0x1b8ab42]  ; -> 02064DB0
004DA26E  mov      rdi, qword ptr [rsp + 0x188]
004DA276  mov      rsi, qword ptr [rsp + 0x180]
004DA27E  movzx    r8d, r15w
004DA282  lea      eax, [rdx + 3]
004DA285  mov      word ptr [rip + 0x1b8ab44], bx  ; -> 02064DD0
004DA28C  shl      eax, 4
004DA28F  movsxd   rcx, eax
004DA292  lea      eax, [rdx + 6]
004DA295  shl      eax, 4
004DA298  mov      rdx, rdi
004DA29B  mov      dword ptr [rcx + r14 + 0xc], r8d
004DA2A0  movsxd   rcx, eax
004DA2A3  mov      dword ptr [rcx + r14 + 0xc], r8d
004DA2A8  mov      rcx, rsi
004DA2AB  call     0x4d7b10  ; -> 004D7B10 fn
004DA2B0  movsx    ebx, word ptr [rip + 0x1b8a855]  ; -> 02064B0C
004DA2B7  lea      eax, [rbx + 4]
004DA2BA  shl      eax, 4
004DA2BD  lea      ecx, [rbx + 1]
004DA2C0  cdqe     
004DA2C2  mov      word ptr [rip + 0x1b8ab1f], cx  ; -> 02064DE8
004DA2C9  movzx    eax, word ptr [rax + r14 + 4]
004DA2CF  and      ax, cx
004DA2D2  mov      word ptr [rip + 0x1b8aaf7], ax  ; -> 02064DD0
004DA2D9  movzx    eax, word ptr [rip + 0x1b8aae4]  ; -> 02064DC4
004DA2E0  test     ax, ax
004DA2E3  jle      0x4da348  ; -> 004DA348
004DA2E5  movss    xmm0, dword ptr [rip + 0x1b8a937]  ; -> 02064C24
004DA2ED  xor      esi, esi
004DA2EF  movss    xmm3, dword ptr [rip + 0x1b8a95d]  ; -> 02064C54
004DA2F7  movss    xmm8, dword ptr [rip + 0x192853c]  ; -> 01E0283C [f32 1]
004DA300  movss    xmm9, dword ptr [rip + 0x1928527]  ; -> 01E02830 [u32 0x00000000]
004DA309  movzx    r13d, word ptr [rip + 0x1b8aaaf]  ; -> 02064DC0
004DA311  movzx    r15d, word ptr [rip + 0x1b8aabb]  ; -> 02064DD4
004DA319  movups   xmmword ptr [rsp + 0x50], xmm0
004DA31E  movss    xmm0, dword ptr [rip + 0x1b8a91e]  ; -> 02064C44
004DA326  movss    dword ptr [rsp + 0x198], xmm0
004DA32F  movss    xmm0, dword ptr [rip + 0x1b8a909]  ; -> 02064C40
004DA337  movss    dword ptr [rsp + 0x20], xmm0
004DA33D  movss    dword ptr [rsp + 0x24], xmm3
004DA343  jmp      0x4d9020  ; -> 004D9020
004DA348  add      bx, 0x12
004DA34C  xor      r8d, r8d
004DA34F  movsx    eax, bx
004DA352  mov      rdx, rdi
004DA355  shl      eax, 4
004DA358  movsxd   rcx, eax
004DA35B  add      rcx, r14
004DA35E  mov      word ptr [rip + 0x1b8aa83], bx  ; -> 02064DE8
004DA365  mov      rax, rsi
004DA368  lea      r11, [rsp + 0x138]
004DA370  movaps   xmm6, xmmword ptr [r11 - 0x18]
004DA375  movaps   xmm7, xmmword ptr [r11 - 0x28]
004DA37A  movaps   xmm8, xmmword ptr [r11 - 0x38]
004DA37F  movaps   xmm9, xmmword ptr [r11 - 0x48]
004DA384  movaps   xmm10, xmmword ptr [r11 - 0x58]
004DA389  movaps   xmm11, xmmword ptr [r11 - 0x68]
004DA38E  movaps   xmm12, xmmword ptr [r11 - 0x78]
004DA393  movaps   xmm13, xmmword ptr [r11 - 0x88]
004DA39B  movaps   xmm14, xmmword ptr [r11 - 0x98]
004DA3A3  movaps   xmm15, xmmword ptr [r11 - 0xa8]
004DA3AB  mov      rsp, r11
004DA3AE  pop      r15
```

## 004DB350 (4953 B, extent 004DB350-004DC6A9)

Page context: "r.md)'s template census decodes; §2.4b there reads the rest of this chain and gives the map — type ''h'' installs '004DF440' and '004E0F70', ''i'' installs '004DCC00' and '004DDDF0', '0xA3' installs '004DB350', '0xA6' and '0xA8' share '004DA8A0', and ''j'' installs '004D7BF0'. **The copied template carries the MPG descriptor verbatim**, which is how the program reaches the packet at all: the builder only re-points the *data* descriptor "

```
004DB350  mov      rax, rsp
004DB353  mov      qword ptr [rax + 0x10], rbx
004DB357  push     rbp
004DB358  push     rsi
004DB359  push     rdi
004DB35A  push     r12
004DB35C  push     r13
004DB35E  push     r14
004DB360  push     r15
004DB362  sub      rsp, 0xd0
004DB369  movaps   xmmword ptr [rax - 0x48], xmm6
004DB36D  lea      r14, [rip + 0x1b89abc]  ; -> 02064E30
004DB374  movaps   xmmword ptr [rax - 0x58], xmm7
004DB378  mov      r12, rcx
004DB37B  movaps   xmmword ptr [rax - 0x68], xmm8
004DB380  xor      r8d, r8d
004DB383  movaps   xmmword ptr [rax - 0x78], xmm9
004DB388  mov      r15, rdx
004DB38B  movaps   xmmword ptr [rax - 0x88], xmm10
004DB393  movzx    eax, word ptr [rip + 0x1b89772]  ; -> 02064B0C
004DB39A  add      ax, 0xb
004DB39E  movaps   xmmword ptr [rsp + 0x70], xmm11
004DB3A4  mov      word ptr [rip + 0x1b89a3d], ax  ; -> 02064DE8
004DB3AB  movaps   xmmword ptr [rsp + 0x60], xmm12
004DB3B1  cwde     
004DB3B2  shl      eax, 4
004DB3B5  movsxd   rcx, eax
004DB3B8  movaps   xmmword ptr [rsp + 0x50], xmm13
004DB3BE  add      rcx, r14
004DB3C1  movaps   xmmword ptr [rsp + 0x40], xmm14
004DB3C7  movaps   xmmword ptr [rsp + 0x30], xmm15
004DB3CD  call     r12
004DB3D0  movsx    r8d, word ptr [rip + 0x1b89734]  ; -> 02064B0C
004DB3D8  xorps    xmm6, xmm6
004DB3DB  movss    xmm14, dword ptr [rip + 0x1927458]  ; -> 01E0283C [f32 1]
004DB3E4  mov      r9d, r8d
004DB3E7  movss    xmm12, dword ptr [rip + 0x424f70]  ; -> 00900360 [u32 0x7F7FFFFF]
004DB3F0  mov      edx, r8d
004DB3F3  shl      r9d, 4
004DB3F7  lea      eax, [r8 + 3]
004DB3FB  mov      word ptr [rip + 0x1b899b5], r8w  ; -> 02064DB8
004DB403  shl      eax, 4
004DB406  movsxd   rcx, eax
004DB409  mov      eax, 0x334
004DB40E  add      eax, r8d
004DB411  mov      word ptr [rip + 0x1b899b7], r8w  ; -> 02064DD0
004DB419  mov      word ptr [rip + 0x1b89990], ax  ; -> 02064DB0
004DB420  inc      ax
004DB423  mov      word ptr [rip + 0x1b8998a], ax  ; -> 02064DB4
004DB42A  movups   xmm0, xmmword ptr [rcx + r14]
004DB42F  movsxd   rax, r9d
004DB432  movups   xmmword ptr [rip + 0x1b89727], xmm0  ; -> 02064B60
004DB439  movss    xmm2, dword ptr [rip + 0x1b89727]  ; -> 02064B68
004DB441  movups   xmm1, xmm0
004DB444  movzx    eax, word ptr [rax + r14 + 0xc]
004DB44A  subss    xmm2, dword ptr [rip + 0x1b8970e]  ; -> 02064B60
004DB452  shufps   xmm1, xmm1, 0x55
004DB456  shufps   xmm0, xmm0, 0xff
004DB45A  subss    xmm0, xmm1
004DB45E  mov      word ptr [rip + 0x1b8996f], ax  ; -> 02064DD4
004DB465  lea      eax, [r8 + 0x14]
004DB469  ucomiss  xmm2, xmm6
004DB46C  mov      word ptr [rip + 0x1b89949], ax  ; -> 02064DBC
004DB473  movss    dword ptr [rip + 0x1b896f1], xmm0  ; -> 02064B6C
004DB47B  jp       0x4db485  ; -> 004DB485
004DB47D  jne      0x4db485  ; -> 004DB485
004DB47F  movaps   xmm3, xmm12
004DB483  jmp      0x4db48d  ; -> 004DB48D
004DB485  movaps   xmm3, xmm14
004DB489  divss    xmm3, xmm2
004DB48D  lea      eax, [rdx + 4]
004DB490  movss    dword ptr [rip + 0x1b89668], xmm3  ; -> 02064B00
004DB498  shl      eax, 4
004DB49B  movsxd   rcx, eax
004DB49E  lea      eax, [rdx + 5]
004DB4A1  shl      eax, 4
004DB4A4  mov      word ptr [rip + 0x1b89918], r8w  ; -> 02064DC4
004DB4AC  movups   xmm1, xmmword ptr [rcx + r14]
004DB4B1  movsxd   rcx, eax
004DB4B4  lea      eax, [r9 + 0x10]
004DB4B8  cvtdq2ps xmm1, xmm1
004DB4BB  movups   xmm2, xmmword ptr [rcx + r14]
004DB4C0  movsxd   rcx, eax
004DB4C3  lea      eax, [rdx + 0xa]
004DB4C6  shl      eax, 4
004DB4C9  movups   xmmword ptr [rip + 0x1b896f0], xmm1  ; -> 02064BC0
004DB4D0  movups   xmm0, xmmword ptr [rcx + r14]
004DB4D5  movsxd   rcx, eax
004DB4D8  lea      eax, [rdx + 6]
004DB4DB  shl      eax, 4
004DB4DE  movups   xmmword ptr [rip + 0x1b8964b], xmm0  ; -> 02064B30
004DB4E5  movups   xmm0, xmmword ptr [rcx + r14]
004DB4EA  movsxd   rcx, eax
004DB4ED  lea      eax, [rdx + 7]
004DB4F0  shl      eax, 4
004DB4F3  movups   xmmword ptr [rip + 0x1b89656], xmm0  ; -> 02064B50
004DB4FA  movups   xmm0, xmmword ptr [rcx + r14]
004DB4FF  movsxd   rcx, eax
004DB502  lea      eax, [rdx + 8]
004DB505  shl      eax, 4
004DB508  movups   xmmword ptr [rip + 0x1b897d1], xmm0  ; -> 02064CE0
004DB50F  movups   xmm0, xmmword ptr [rcx + r14]
004DB514  movsxd   rcx, eax
004DB517  lea      eax, [rdx + 9]
004DB51A  shl      eax, 4
004DB51D  movups   xmmword ptr [rip + 0x1b897cc], xmm0  ; -> 02064CF0
004DB524  movups   xmm0, xmmword ptr [rcx + r14]
004DB529  movsxd   rcx, eax
004DB52C  lea      eax, [rdx + 2]
004DB52F  shl      eax, 4
004DB532  movups   xmmword ptr [rip + 0x1b897c7], xmm0  ; -> 02064D00
004DB539  movups   xmm0, xmmword ptr [rcx + r14]
004DB53E  movsxd   rcx, eax
004DB541  movups   xmmword ptr [rip + 0x1b897c8], xmm0  ; -> 02064D10
004DB548  movzx    r9d, word ptr [rcx + r14]
004DB54D  cvtdq2ps xmm0, xmm2
004DB550  mov      word ptr [rip + 0x1b89868], r9w  ; -> 02064DC0
004DB558  movups   xmmword ptr [rip + 0x1b89671], xmm0  ; -> 02064BD0
004DB55F  movss    xmm0, dword ptr [rip + 0x19272d1]  ; -> 01E02838 [u32 0x00000000]
004DB567  addss    xmm0, xmm3
004DB56B  ucomiss  xmm0, xmm6
004DB56E  movss    dword ptr [rip + 0x1b895f2], xmm0  ; -> 02064B68
004DB576  jp       0x4db5a0  ; -> 004DB5A0
004DB578  jne      0x4db5a0  ; -> 004DB5A0
004DB57A  call     0x22cc40  ; -> 0022CC40 fn
004DB57F  movss    xmm0, dword ptr [rip + 0x1b895e1]  ; -> 02064B68
004DB587  movzx    r9d, word ptr [rip + 0x1b89831]  ; -> 02064DC0
004DB58F  movzx    r8d, word ptr [rip + 0x1b8982d]  ; -> 02064DC4
004DB597  movss    xmm14, dword ptr [rip + 0x192729c]  ; -> 01E0283C [f32 1]
004DB5A0  comiss   xmm6, xmm0
004DB5A3  jbe      0x4db5c3  ; -> 004DB5C3
004DB5A5  call     0x22cc30  ; -> 0022CC30 fn
004DB5AA  movzx    r9d, word ptr [rip + 0x1b8980e]  ; -> 02064DC0
004DB5B2  movzx    r8d, word ptr [rip + 0x1b8980a]  ; -> 02064DC4
004DB5BA  movss    xmm14, dword ptr [rip + 0x1927279]  ; -> 01E0283C [f32 1]
004DB5C3  xor      r13d, r13d
004DB5C6  movsd    xmm15, qword ptr [rip + 0x18107b1]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004DB5CF  mov      edi, 0xe0
004DB5D4  movsx    edx, r8w
004DB5D8  add      r8w, 4
004DB5DD  mov      word ptr [rip + 0x1b897df], r8w  ; -> 02064DC4
004DB5E5  lea      eax, [rdx + 0x14]
004DB5E8  shl      eax, 4
004DB5EB  movsxd   rcx, eax
004DB5EE  lea      eax, [rdx + 0x16]
004DB5F1  shl      eax, 4
004DB5F4  movups   xmm10, xmmword ptr [rcx + r14]
004DB5F9  movsxd   rcx, eax
004DB5FC  lea      eax, [rdx + 0x15]
004DB5FF  shl      eax, 4
004DB602  movaps   xmm4, xmm10
004DB606  movaps   xmm7, xmm10
004DB60A  shufps   xmm7, xmm10, 0xaa
004DB60F  movaps   xmm8, xmm10
004DB613  movups   xmm9, xmmword ptr [rcx + r14]
004DB618  movsxd   rcx, eax
004DB61B  lea      eax, [rdx + 0x17]
004DB61E  movaps   xmm2, xmm7
004DB621  shufps   xmm8, xmm10, 0x55
004DB626  subss    xmm7, dword ptr [rip + 0x1b8952a]  ; -> 02064B58
004DB62E  mulss    xmm2, xmm14
004DB633  movaps   xmm3, xmm8
004DB637  shl      eax, 4
004DB63A  movups   xmm5, xmmword ptr [rcx + r14]
004DB63F  movsxd   rcx, eax
004DB642  add      r9w, -2
004DB647  subss    xmm8, dword ptr [rip + 0x1b89504]  ; -> 02064B54
004DB650  movups   xmmword ptr [rip + 0x1b895c9], xmm5  ; -> 02064C20
004DB657  mov      word ptr [rip + 0x1b89761], r9w  ; -> 02064DC0
004DB65F  mulss    xmm3, xmm14
004DB664  movaps   xmm1, xmm5
004DB667  movups   xmm6, xmmword ptr [rcx + r14]
004DB66C  shufps   xmm1, xmm5, 0xff
004DB670  movaps   xmm0, xmm1
004DB673  mulss    xmm4, xmm14
004DB678  mulss    xmm0, xmm5
004DB67C  movups   xmmword ptr [rip + 0x1b895ad], xmm6  ; -> 02064C30
004DB683  addss    xmm0, xmm4
004DB687  movss    dword ptr [rip + 0x1b8959c], xmm14  ; -> 02064C2C
004DB690  movups   xmmword ptr [rip + 0x1b89558], xmm9  ; -> 02064BF0
004DB698  movups   xmmword ptr [rip + 0x1b89540], xmm10  ; -> 02064BE0
004DB6A0  subss    xmm10, dword ptr [rip + 0x1b894a7]  ; -> 02064B50
004DB6A9  movss    dword ptr [rip + 0x1b8956f], xmm0  ; -> 02064C20
004DB6B1  movaps   xmm0, xmm1
004DB6B4  mulss    xmm0, dword ptr [rip + 0x1b89568]  ; -> 02064C24
004DB6BC  mulss    xmm1, dword ptr [rip + 0x1b89564]  ; -> 02064C28
004DB6C4  addss    xmm0, xmm3
004DB6C8  movss    dword ptr [rip + 0x1b8951b], xmm14  ; -> 02064BEC
004DB6D1  movaps   xmm3, xmm9
004DB6D5  movss    dword ptr [rip + 0x1b8951e], xmm14  ; -> 02064BFC
004DB6DE  addss    xmm1, xmm2
004DB6E2  shufps   xmm3, xmm9, 0x55
004DB6E7  movaps   xmm2, xmm9
004DB6EB  mulss    xmm3, xmm14
004DB6F0  movss    dword ptr [rip + 0x1b8952c], xmm0  ; -> 02064C24
004DB6F8  mulss    xmm2, xmm14
004DB6FD  movss    dword ptr [rip + 0x1b89523], xmm1  ; -> 02064C28
004DB705  movaps   xmm1, xmm6
004DB708  shufps   xmm1, xmm6, 0xff
004DB70C  movaps   xmm0, xmm1
004DB70F  shufps   xmm9, xmm9, 0xaa
004DB714  mulss    xmm0, xmm6
004DB718  mulss    xmm9, xmm14
004DB71D  addss    xmm0, xmm2
004DB721  movss    dword ptr [rip + 0x1b893f7], xmm2  ; -> 02064B20
004DB729  movss    dword ptr [rip + 0x1b893f3], xmm3  ; -> 02064B24
004DB731  movss    dword ptr [rip + 0x1b893ee], xmm9  ; -> 02064B28
004DB73A  movss    dword ptr [rip + 0x1b894f9], xmm14  ; -> 02064C3C
004DB743  movss    dword ptr [rip + 0x1b894b4], xmm10  ; -> 02064C00
004DB74C  movss    dword ptr [rip + 0x1b894dc], xmm0  ; -> 02064C30
004DB754  movaps   xmm0, xmm1
004DB757  mulss    xmm0, dword ptr [rip + 0x1b894d5]  ; -> 02064C34
004DB75F  mulss    xmm1, dword ptr [rip + 0x1b894d1]  ; -> 02064C38
004DB767  addss    xmm0, xmm3
004DB76B  movss    dword ptr [rip + 0x1b89490], xmm8  ; -> 02064C04
004DB774  movss    dword ptr [rip + 0x1b8948c], xmm7  ; -> 02064C08
004DB77C  addss    xmm1, xmm9
004DB781  movss    dword ptr [rip + 0x1b894ab], xmm0  ; -> 02064C34
004DB789  movss    dword ptr [rip + 0x1b894a7], xmm1  ; -> 02064C38
004DB791  call     0x22cc20  ; -> 0022CC20 fn
004DB796  movups   xmm0, xmmword ptr [rip + 0x1b89423]  ; -> 02064BC0
004DB79D  movss    xmm1, dword ptr [rip + 0x1b8944f]  ; -> 02064BF4
004DB7A5  subss    xmm1, dword ptr [rip + 0x1b893a7]  ; -> 02064B54
004DB7AD  movups   xmmword ptr [rip + 0x1b8948c], xmm0  ; -> 02064C40
004DB7B4  movss    xmm0, dword ptr [rip + 0x1b89434]  ; -> 02064BF0
004DB7BC  subss    xmm0, dword ptr [rip + 0x1b8938c]  ; -> 02064B50
004DB7C4  movss    dword ptr [rip + 0x1b89448], xmm1  ; -> 02064C14
004DB7CC  movss    dword ptr [rip + 0x1b8943c], xmm0  ; -> 02064C10
004DB7D4  movss    xmm0, dword ptr [rip + 0x1b8941c]  ; -> 02064BF8
004DB7DC  subss    xmm0, dword ptr [rip + 0x1b89374]  ; -> 02064B58
004DB7E4  movss    dword ptr [rip + 0x1b8942c], xmm0  ; -> 02064C18
004DB7EC  call     0x22cc20  ; -> 0022CC20 fn
004DB7F1  movss    xmm14, dword ptr [rip + 0x1927042]  ; -> 01E0283C [f32 1]
004DB7FA  movss    xmm1, dword ptr [rip + 0x1b893c2]  ; -> 02064BC4
004DB802  movss    xmm4, dword ptr [rip + 0x1b893fa]  ; -> 02064C04
004DB80A  movss    xmm0, dword ptr [rip + 0x1b893ae]  ; -> 02064BC0
004DB812  movss    xmm7, dword ptr [rip + 0x1b893ee]  ; -> 02064C08
004DB81A  movss    xmm5, dword ptr [rip + 0x1b893ae]  ; -> 02064BD0
004DB822  movss    xmm3, dword ptr [rip + 0x1b893aa]  ; -> 02064BD4
004DB82A  movss    xmm2, dword ptr [rip + 0x1b893a6]  ; -> 02064BD8
004DB832  movss    xmm6, dword ptr [rip + 0x1b893c6]  ; -> 02064C00
004DB83A  movss    xmm11, dword ptr [rip + 0x1b893d5]  ; -> 02064C18
004DB843  movss    dword ptr [rip + 0x1b89415], xmm0  ; -> 02064C60
004DB84B  movss    xmm0, dword ptr [rip + 0x1b89375]  ; -> 02064BC8
004DB853  movss    dword ptr [rip + 0x1b8940d], xmm0  ; -> 02064C68
004DB85B  movss    xmm0, dword ptr [rip + 0x1b893b1]  ; -> 02064C14
004DB863  mulss    xmm0, xmm0
004DB867  movss    dword ptr [rip + 0x1b893f5], xmm1  ; -> 02064C64
004DB86F  movss    xmm1, dword ptr [rip + 0x1b89399]  ; -> 02064C10
004DB877  movss    dword ptr [rip + 0x1b89415], xmm0  ; -> 02064C94
004DB87F  mulss    xmm0, xmm14
004DB884  mulss    xmm7, xmm7
004DB888  mulss    xmm4, xmm4
004DB88C  mulss    xmm1, xmm1
004DB890  mulss    xmm11, xmm11
004DB895  mulss    xmm6, xmm6
004DB899  movss    dword ptr [rip + 0x1b893e3], xmm4  ; -> 02064C84
004DB8A1  mulss    xmm4, xmm14
004DB8A6  movss    dword ptr [rip + 0x1b893da], xmm7  ; -> 02064C88
004DB8AE  mulss    xmm7, xmm14
004DB8B3  mulss    xmm1, xmm14
004DB8B8  movss    dword ptr [rip + 0x1b893d7], xmm11  ; -> 02064C98
004DB8C1  mulss    xmm6, xmm14
004DB8C6  addss    xmm1, xmm0
004DB8CA  mulss    xmm11, xmm14
004DB8CF  addss    xmm6, xmm4
004DB8D3  movss    dword ptr [rip + 0x1b89375], xmm5  ; -> 02064C50
004DB8DB  movss    dword ptr [rip + 0x1b89371], xmm3  ; -> 02064C54
004DB8E3  movss    dword ptr [rip + 0x1b8936d], xmm2  ; -> 02064C58
004DB8EB  addss    xmm11, xmm1
004DB8F0  movss    dword ptr [rip + 0x1b89378], xmm5  ; -> 02064C70
004DB8F8  movss    dword ptr [rip + 0x1b89374], xmm3  ; -> 02064C74
004DB900  addss    xmm7, xmm6
004DB904  movss    dword ptr [rip + 0x1b8936c], xmm2  ; -> 02064C78
004DB90C  movss    dword ptr [rip + 0x1b89387], xmm11  ; -> 02064C9C
004DB915  cvtps2pd xmm0, xmm7
004DB918  movss    dword ptr [rip + 0x1b8936c], xmm7  ; -> 02064C8C
004DB920  andps    xmm0, xmm15
004DB924  cvtpd2ps xmm0, xmm0
004DB928  call     0x861f14  ; -> 00861F14 fn
004DB92D  movss    xmm13, dword ptr [rip + 0x1926efa]  ; -> 01E02830 [u32 0x00000000]
004DB936  movaps   xmm10, xmm0
004DB93A  addss    xmm10, xmm13
004DB93F  cvtps2pd xmm0, xmm11
004DB943  subss    xmm10, dword ptr [rip + 0x1b89214]  ; -> 02064B60
004DB94C  andps    xmm0, xmm15
004DB950  cvtpd2ps xmm0, xmm0
004DB954  mulss    xmm10, dword ptr [rip + 0x1b8920b]  ; -> 02064B68
004DB95D  minss    xmm10, xmm14
004DB962  maxss    xmm10, xmm13
004DB967  mulss    xmm10, dword ptr [rip + 0x1b891fc]  ; -> 02064B6C
004DB970  addss    xmm10, dword ptr [rip + 0x1b891eb]  ; -> 02064B64
004DB979  movss    dword ptr [rip + 0x1b892fe], xmm10  ; -> 02064C80
004DB982  call     0x861f14  ; -> 00861F14 fn
004DB987  movaps   xmm3, xmm0
004DB98A  addss    xmm3, xmm13
004DB98F  subss    xmm3, dword ptr [rip + 0x1b891c9]  ; -> 02064B60
004DB997  mulss    xmm3, dword ptr [rip + 0x1b891c9]  ; -> 02064B68
004DB99F  minss    xmm3, xmm14
004DB9A4  maxss    xmm3, xmm13
004DB9A9  mulss    xmm3, dword ptr [rip + 0x1b891bb]  ; -> 02064B6C
004DB9B1  movss    xmm0, dword ptr [rip + 0x1b89293]  ; -> 02064C4C
004DB9B9  movss    xmm2, dword ptr [rip + 0x1b8921b]  ; -> 02064BDC
004DB9C1  addss    xmm3, dword ptr [rip + 0x1b8919b]  ; -> 02064B64
004DB9C9  movss    xmm6, dword ptr [rip + 0x1b8920f]  ; -> 02064BE0
004DB9D1  movss    xmm1, dword ptr [rip + 0x1b891f3]  ; -> 02064BCC
004DB9D9  movss    xmm15, dword ptr [rip + 0x1b8930e]  ; -> 02064CF0
004DB9E2  movss    xmm9, dword ptr [rip + 0x1b89325]  ; -> 02064D10
004DB9EB  movss    xmm11, dword ptr [rip + 0x1b89324]  ; -> 02064D18
004DB9F4  movss    xmm8, dword ptr [rip + 0x1b8931f]  ; -> 02064D1C
004DB9FD  mulss    xmm0, xmm10
004DBA02  mulss    xmm1, xmm3
004DBA06  movss    dword ptr [rip + 0x1b8923e], xmm0  ; -> 02064C4C
004DBA0E  movaps   xmm0, xmm2
004DBA11  mulss    xmm0, xmm10
004DBA16  movss    xmm10, dword ptr [rip + 0x1b892f5]  ; -> 02064D14
004DBA1F  movss    dword ptr [rip + 0x1b89245], xmm1  ; -> 02064C6C
004DBA27  movss    dword ptr [rip + 0x1b8922d], xmm0  ; -> 02064C5C
004DBA2F  movups   xmm0, xmmword ptr [rip + 0x1b892aa]  ; -> 02064CE0
004DBA36  mulss    xmm2, xmm3
004DBA3A  shufps   xmm6, xmm6, 0
004DBA3E  mulps    xmm6, xmm0
004DBA41  movaps   xmm0, xmm15
004DBA45  movss    dword ptr [rip + 0x1b8922f], xmm2  ; -> 02064C7C
004DBA4D  movss    xmm2, dword ptr [rip + 0x1b8918f]  ; -> 02064BE4
004DBA55  mulss    xmm0, xmm2
004DBA59  movups   xmmword ptr [rip + 0x1b890c0], xmm6  ; -> 02064B20
004DBA60  movss    xmm5, dword ptr [rip + 0x1b890c4]  ; -> 02064B2C
004DBA68  addss    xmm6, xmm0
004DBA6C  movss    xmm0, dword ptr [rip + 0x1b89280]  ; -> 02064CF4
004DBA74  movss    xmm4, dword ptr [rip + 0x1b890ac]  ; -> 02064B28
004DBA7C  movss    dword ptr [rsp + 0x110], xmm0
004DBA85  mulss    xmm0, xmm2
004DBA89  movss    dword ptr [rip + 0x1b891ff], xmm3  ; -> 02064C90
004DBA91  movss    xmm3, dword ptr [rip + 0x1b8908b]  ; -> 02064B24
004DBA99  addss    xmm3, xmm0
004DBA9D  movss    xmm0, dword ptr [rip + 0x1b89253]  ; -> 02064CF8
004DBAA5  movaps   xmm1, xmm0
004DBAA8  movss    dword ptr [rsp + 0x120], xmm0
004DBAB1  movss    xmm0, dword ptr [rip + 0x1b89243]  ; -> 02064CFC
004DBAB9  movss    dword ptr [rsp + 0x128], xmm0
004DBAC2  mulss    xmm0, xmm2
004DBAC6  mulss    xmm1, xmm2
004DBACA  movss    xmm2, dword ptr [rip + 0x1b89116]  ; -> 02064BE8
004DBAD2  addss    xmm5, xmm0
004DBAD6  movss    xmm0, dword ptr [rip + 0x1b89222]  ; -> 02064D00
004DBADE  movss    dword ptr [rsp + 0x20], xmm0
004DBAE4  addss    xmm4, xmm1
004DBAE8  movaps   xmm1, xmm0
004DBAEB  movss    xmm0, dword ptr [rip + 0x1b89211]  ; -> 02064D04
004DBAF3  movss    dword ptr [rsp + 0x24], xmm0
004DBAF9  mulss    xmm0, xmm2
004DBAFD  mulss    xmm1, xmm2
004DBB01  addss    xmm3, xmm0
004DBB05  movss    xmm0, dword ptr [rip + 0x1b891fb]  ; -> 02064D08
004DBB0D  movss    dword ptr [rsp + 0x28], xmm0
004DBB13  addss    xmm6, xmm1
004DBB17  movaps   xmm1, xmm0
004DBB1A  movss    xmm0, dword ptr [rip + 0x1b891ea]  ; -> 02064D0C
004DBB22  movss    dword ptr [rsp + 0x2c], xmm0
004DBB28  mulss    xmm1, xmm2
004DBB2C  mulss    xmm2, xmm0
004DBB30  movaps   xmm0, xmm9
004DBB34  addss    xmm4, xmm1
004DBB38  movaps   xmm1, xmm11
004DBB3C  addss    xmm5, xmm2
004DBB40  movss    xmm2, dword ptr [rip + 0x1b890a4]  ; -> 02064BEC
004DBB48  mulss    xmm0, xmm2
004DBB4C  mulss    xmm1, xmm2
004DBB50  addss    xmm0, xmm6
004DBB54  addss    xmm1, xmm4
004DBB58  movss    dword ptr [rip + 0x1b89080], xmm0  ; -> 02064BE0
004DBB60  movaps   xmm0, xmm10
004DBB64  mulss    xmm0, xmm2
004DBB68  movss    dword ptr [rip + 0x1b89078], xmm1  ; -> 02064BE8
004DBB70  addss    xmm0, xmm3
004DBB74  movss    dword ptr [rip + 0x1b89068], xmm0  ; -> 02064BE4
004DBB7C  movaps   xmm0, xmm8
004DBB80  mulss    xmm0, xmm2
004DBB84  addss    xmm0, xmm5
004DBB88  movss    dword ptr [rip + 0x1b8905c], xmm0  ; -> 02064BEC
004DBB90  ucomiss  xmm0, dword ptr [rip + 0x425ded]  ; -> 00901984 [u32 0x00000000]
004DBB97  jp       0x4dbb9b  ; -> 004DBB9B
004DBB99  je       0x4dbba4  ; -> 004DBBA4
004DBB9B  movaps   xmm12, xmm14
004DBB9F  divss    xmm12, xmm0
004DBBA4  movss    xmm2, dword ptr [rip + 0x1b89048]  ; -> 02064BF4
004DBBAC  movss    xmm3, dword ptr [rip + 0x1b89048]  ; -> 02064BFC
004DBBB4  movss    xmm7, dword ptr [rip + 0x1b89034]  ; -> 02064BF0
004DBBBC  movups   xmm0, xmmword ptr [rip + 0x1b8911d]  ; -> 02064CE0
004DBBC3  movss    xmm1, dword ptr [rsp + 0x120]
004DBBCC  mulss    xmm1, xmm2
004DBBD0  shufps   xmm7, xmm7, 0
004DBBD4  mulps    xmm7, xmm0
004DBBD7  movaps   xmm0, xmm15
004DBBDB  mulss    xmm0, xmm2
004DBBDF  movups   xmmword ptr [rip + 0x1b88f3a], xmm7  ; -> 02064B20
004DBBE6  movss    xmm4, dword ptr [rip + 0x1b88f36]  ; -> 02064B24
004DBBEE  addss    xmm7, xmm0
004DBBF2  movss    xmm0, dword ptr [rsp + 0x110]
004DBBFB  movss    xmm6, dword ptr [rip + 0x1b88f29]  ; -> 02064B2C
004DBC03  movss    xmm5, dword ptr [rip + 0x1b88f1d]  ; -> 02064B28
004DBC0B  mulss    xmm0, xmm2
004DBC0F  addss    xmm5, xmm1
004DBC13  movss    xmm1, dword ptr [rsp + 0x20]
004DBC19  addss    xmm4, xmm0
004DBC1D  movss    xmm0, dword ptr [rsp + 0x128]
004DBC26  mulss    xmm0, xmm2
004DBC2A  movss    xmm2, dword ptr [rip + 0x1b88fc6]  ; -> 02064BF8
004DBC32  mulss    xmm1, xmm2
004DBC36  addss    xmm6, xmm0
004DBC3A  movss    xmm0, dword ptr [rsp + 0x24]
004DBC40  mulss    xmm0, xmm2
004DBC44  addss    xmm7, xmm1
004DBC48  movss    xmm1, dword ptr [rsp + 0x28]
004DBC4E  mulss    xmm1, xmm2
004DBC52  mulss    xmm2, dword ptr [rsp + 0x2c]
004DBC58  addss    xmm4, xmm0
004DBC5C  addss    xmm5, xmm1
004DBC60  movaps   xmm0, xmm9
004DBC64  mulss    xmm0, xmm3
004DBC68  movaps   xmm1, xmm11
004DBC6C  addss    xmm6, xmm2
004DBC70  mulss    xmm1, xmm3
004DBC74  addss    xmm0, xmm7
004DBC78  movaps   xmm2, xmm8
004DBC7C  movups   xmm7, xmmword ptr [rip + 0x1b88f5d]  ; -> 02064BE0
004DBC83  mulss    xmm2, xmm3
004DBC87  addss    xmm1, xmm5
004DBC8B  movss    dword ptr [rip + 0x1b88f5d], xmm0  ; -> 02064BF0
004DBC93  movaps   xmm0, xmm10
004DBC97  mulss    xmm0, xmm3
004DBC9B  addss    xmm2, xmm6
004DBC9F  movss    dword ptr [rip + 0x1b88f51], xmm1  ; -> 02064BF8
004DBCA7  addss    xmm0, xmm4
004DBCAB  ucomiss  xmm2, dword ptr [rip + 0x425cd2]  ; -> 00901984 [u32 0x00000000]
004DBCB2  movss    dword ptr [rip + 0x1b88f3a], xmm0  ; -> 02064BF4
004DBCBA  movaps   xmm0, xmm12
004DBCBE  shufps   xmm0, xmm0, 0
004DBCC2  mulps    xmm7, xmm0
004DBCC5  movss    dword ptr [rip + 0x1b88f2f], xmm2  ; -> 02064BFC
004DBCCD  jp       0x4dbcdc  ; -> 004DBCDC
004DBCCF  jne      0x4dbcdc  ; -> 004DBCDC
004DBCD1  movss    xmm12, dword ptr [rip + 0x424686]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBCDA  jmp      0x4dbce5  ; -> 004DBCE5
004DBCDC  movaps   xmm12, xmm14
004DBCE0  divss    xmm12, xmm2
004DBCE5  movss    xmm2, dword ptr [rip + 0x1b88f37]  ; -> 02064C24
004DBCED  movss    xmm6, dword ptr [rip + 0x1b88f2b]  ; -> 02064C20
004DBCF5  movups   xmm0, xmmword ptr [rip + 0x1b88fe4]  ; -> 02064CE0
004DBCFC  movss    xmm1, dword ptr [rsp + 0x120]
004DBD05  mulss    xmm1, xmm2
004DBD09  shufps   xmm6, xmm6, 0
004DBD0D  mulps    xmm6, xmm0
004DBD10  movaps   xmm0, xmm15
004DBD14  mulss    xmm0, xmm2
004DBD18  movups   xmmword ptr [rip + 0x1b88e01], xmm6  ; -> 02064B20
004DBD1F  movss    xmm3, dword ptr [rip + 0x1b88dfd]  ; -> 02064B24
004DBD27  addss    xmm6, xmm0
004DBD2B  movss    xmm0, dword ptr [rsp + 0x110]
004DBD34  movss    xmm5, dword ptr [rip + 0x1b88df0]  ; -> 02064B2C
004DBD3C  movss    xmm4, dword ptr [rip + 0x1b88de4]  ; -> 02064B28
004DBD44  mulss    xmm0, xmm2
004DBD48  addss    xmm4, xmm1
004DBD4C  movss    xmm1, dword ptr [rsp + 0x20]
004DBD52  addss    xmm3, xmm0
004DBD56  movss    xmm0, dword ptr [rsp + 0x128]
004DBD5F  mulss    xmm0, xmm2
004DBD63  movss    xmm2, dword ptr [rip + 0x1b88ebd]  ; -> 02064C28
004DBD6B  mulss    xmm1, xmm2
004DBD6F  addss    xmm5, xmm0
004DBD73  movss    xmm0, dword ptr [rsp + 0x24]
004DBD79  mulss    xmm0, xmm2
004DBD7D  addss    xmm6, xmm1
004DBD81  movss    xmm1, dword ptr [rsp + 0x28]
004DBD87  mulss    xmm1, xmm2
004DBD8B  addss    xmm3, xmm0
004DBD8F  movss    xmm0, dword ptr [rsp + 0x2c]
004DBD95  mulss    xmm0, xmm2
004DBD99  movss    xmm2, dword ptr [rip + 0x1b88e8b]  ; -> 02064C2C
004DBDA1  addss    xmm4, xmm1
004DBDA5  movaps   xmm1, xmm9
004DBDA9  addss    xmm5, xmm0
004DBDAD  mulss    xmm1, xmm2
004DBDB1  movaps   xmm0, xmm10
004DBDB5  mulss    xmm0, xmm2
004DBDB9  addss    xmm1, xmm6
004DBDBD  addss    xmm0, xmm3
004DBDC1  movaps   xmm3, xmm8
004DBDC5  mulss    xmm3, xmm2
004DBDC9  movss    dword ptr [rip + 0x1b88e4f], xmm1  ; -> 02064C20
004DBDD1  movaps   xmm1, xmm11
004DBDD5  mulss    xmm1, xmm2
004DBDD9  addss    xmm3, xmm5
004DBDDD  movss    dword ptr [rip + 0x1b88e3f], xmm0  ; -> 02064C24
004DBDE5  movups   xmm5, xmmword ptr [rip + 0x1b88e04]  ; -> 02064BF0
004DBDEC  addss    xmm1, xmm4
004DBDF0  movaps   xmm0, xmm12
004DBDF4  shufps   xmm0, xmm0, 0
004DBDF8  ucomiss  xmm3, dword ptr [rip + 0x425b85]  ; -> 00901984 [u32 0x00000000]
004DBDFF  movss    dword ptr [rip + 0x1b88e21], xmm1  ; -> 02064C28
004DBE07  movss    dword ptr [rip + 0x1b88e1d], xmm3  ; -> 02064C2C
004DBE0F  mulps    xmm5, xmm0
004DBE12  jp       0x4dbe20  ; -> 004DBE20
004DBE14  jne      0x4dbe20  ; -> 004DBE20
004DBE16  movss    xmm6, dword ptr [rip + 0x424542]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBE1E  jmp      0x4dbe28  ; -> 004DBE28
004DBE20  movaps   xmm6, xmm14
004DBE24  divss    xmm6, xmm3
004DBE28  movss    xmm4, dword ptr [rip + 0x1b88e00]  ; -> 02064C30
004DBE30  movups   xmm0, xmmword ptr [rip + 0x1b88ea9]  ; -> 02064CE0
004DBE37  movss    xmm2, dword ptr [rsp + 0x110]
004DBE40  movss    xmm3, dword ptr [rsp + 0x120]
004DBE49  movss    xmm12, dword ptr [rsp + 0x128]
004DBE53  shufps   xmm4, xmm4, 0
004DBE57  mulps    xmm4, xmm0
004DBE5A  movss    xmm0, dword ptr [rip + 0x1b88dd2]  ; -> 02064C34
004DBE62  mulss    xmm12, xmm0
004DBE67  movups   xmmword ptr [rip + 0x1b88cb2], xmm4  ; -> 02064B20
004DBE6E  movss    xmm1, dword ptr [rip + 0x1b88cae]  ; -> 02064B24
004DBE76  mulss    xmm2, xmm0
004DBE7A  mulss    xmm3, xmm0
004DBE7E  addss    xmm1, xmm2
004DBE82  mulss    xmm15, xmm0
004DBE87  movss    xmm0, dword ptr [rip + 0x1b88da9]  ; -> 02064C38
004DBE8F  movss    xmm2, dword ptr [rip + 0x1b88c91]  ; -> 02064B28
004DBE97  addss    xmm2, xmm3
004DBE9B  movss    xmm3, dword ptr [rip + 0x1b88c89]  ; -> 02064B2C
004DBEA3  addss    xmm3, xmm12
004DBEA8  movss    xmm12, dword ptr [rsp + 0x20]
004DBEAF  mulss    xmm12, xmm0
004DBEB4  addss    xmm4, xmm15
004DBEB9  addss    xmm4, xmm12
004DBEBE  movss    xmm12, dword ptr [rsp + 0x24]
004DBEC5  mulss    xmm12, xmm0
004DBECA  addss    xmm1, xmm12
004DBECF  movss    dword ptr [rip + 0x1b88c49], xmm4  ; -> 02064B20
004DBED7  movss    xmm12, dword ptr [rsp + 0x28]
004DBEDE  mulss    xmm12, xmm0
004DBEE3  movss    dword ptr [rip + 0x1b88c39], xmm1  ; -> 02064B24
004DBEEB  addss    xmm2, xmm12
004DBEF0  movss    xmm12, dword ptr [rsp + 0x2c]
004DBEF7  mulss    xmm12, xmm0
004DBEFC  movss    xmm0, dword ptr [rip + 0x1b88d38]  ; -> 02064C3C
004DBF04  mulss    xmm8, xmm0
004DBF09  mulss    xmm9, xmm0
004DBF0E  addss    xmm3, xmm12
004DBF13  mulss    xmm10, xmm0
004DBF18  mulss    xmm11, xmm0
004DBF1D  addss    xmm9, xmm4
004DBF22  movaps   xmm0, xmm6
004DBF25  movss    dword ptr [rip + 0x1b88bfb], xmm2  ; -> 02064B28
004DBF2D  addss    xmm10, xmm1
004DBF32  shufps   xmm0, xmm0, 0
004DBF36  movups   xmm1, xmmword ptr [rip + 0x1b88ce3]  ; -> 02064C20
004DBF3D  addss    xmm8, xmm3
004DBF42  movss    dword ptr [rip + 0x1b88be2], xmm3  ; -> 02064B2C
004DBF4A  addss    xmm11, xmm2
004DBF4F  movss    dword ptr [rip + 0x1b88cd8], xmm9  ; -> 02064C30
004DBF58  movss    dword ptr [rip + 0x1b88cd3], xmm10  ; -> 02064C34
004DBF61  mulps    xmm1, xmm0
004DBF64  ucomiss  xmm8, dword ptr [rip + 0x425a18]  ; -> 00901984 [u32 0x00000000]
004DBF6C  movss    dword ptr [rip + 0x1b88cc3], xmm11  ; -> 02064C38
004DBF75  movss    dword ptr [rip + 0x1b88cbe], xmm8  ; -> 02064C3C
004DBF7E  jp       0x4dbf9a  ; -> 004DBF9A
004DBF80  jne      0x4dbf9a  ; -> 004DBF9A
004DBF82  movss    xmm12, dword ptr [rip + 0x4243d5]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBF8B  movss    dword ptr [rip + 0x1b88b6c], xmm12  ; -> 02064B00
004DBF94  movaps   xmm10, xmm12
004DBF98  jmp      0x4dbfb5  ; -> 004DBFB5
004DBF9A  movss    xmm12, dword ptr [rip + 0x4243bd]  ; -> 00900360 [u32 0x7F7FFFFF]
004DBFA3  movaps   xmm10, xmm14
004DBFA7  divss    xmm10, xmm8
004DBFAC  movss    dword ptr [rip + 0x1b88b4b], xmm10  ; -> 02064B00
004DBFB5  movss    xmm4, dword ptr [rip + 0x1b88b73]  ; -> 02064B30
004DBFBD  ucomiss  xmm4, xmm7
004DBFC0  jp       0x4dbfca  ; -> 004DBFCA
004DBFC2  mov      r9d, 1
004DBFC8  je       0x4dbfcd  ; -> 004DBFCD
004DBFCA  mov      r9d, r13d
004DBFCD  movss    xmm2, dword ptr [rip + 0x1b88b5f]  ; -> 02064B34
004DBFD5  movaps   xmm0, xmm7
004DBFD8  shufps   xmm0, xmm7, 0x55
004DBFDC  ucomiss  xmm2, xmm0
004DBFDF  jp       0x4dbfe9  ; -> 004DBFE9
004DBFE1  mov      r8d, 1
004DBFE7  je       0x4dbfec  ; -> 004DBFEC
004DBFE9  mov      r8d, r13d
004DBFEC  movss    xmm3, dword ptr [rip + 0x1b88b44]  ; -> 02064B38
004DBFF4  movaps   xmm6, xmm7
004DBFF7  shufps   xmm6, xmm7, 0xaa
004DBFFB  ucomiss  xmm3, xmm6
004DBFFE  jp       0x4dc007  ; -> 004DC007
004DC000  mov      ecx, 1
004DC005  je       0x4dc00a  ; -> 004DC00A
004DC007  mov      ecx, r13d
004DC00A  comiss   xmm7, xmm4
004DC00D  mov      eax, r13d
004DC010  mov      edx, r13d
004DC013  seta     dl
004DC016  add      dx, dx
004DC019  comiss   xmm0, xmm2
004DC01C  seta     al
004DC01F  add      dx, ax
004DC022  mov      eax, r13d
004DC025  add      dx, dx
004DC028  comiss   xmm6, xmm3
004DC02B  seta     al
004DC02E  add      dx, ax
004DC031  shl      dx, 2
004DC035  add      dx, r9w
004DC039  add      dx, dx
004DC03C  add      dx, r8w
004DC040  add      dx, dx
004DC043  add      dx, cx
004DC046  add      dx, dx
004DC049  ucomiss  xmm7, xmm13
004DC04D  jp       0x4dc057  ; -> 004DC057
004DC04F  mov      r10d, 1
004DC055  je       0x4dc05a  ; -> 004DC05A
004DC057  mov      r10d, r13d
004DC05A  movss    xmm9, dword ptr [rip + 0x19267d1]  ; -> 01E02834 [u32 0x00000000]
004DC063  ucomiss  xmm0, xmm9
004DC067  jp       0x4dc071  ; -> 004DC071
004DC069  mov      r8d, 1
004DC06F  je       0x4dc074  ; -> 004DC074
004DC071  mov      r8d, r13d
004DC074  movss    xmm8, dword ptr [rip + 0x19267bb]  ; -> 01E02838 [u32 0x00000000]
004DC07D  ucomiss  xmm6, xmm8
004DC081  jp       0x4dc08a  ; -> 004DC08A
004DC083  mov      ecx, 1
004DC088  je       0x4dc08d  ; -> 004DC08D
004DC08A  mov      ecx, r13d
004DC08D  comiss   xmm13, xmm7
004DC091  mov      eax, r13d
004DC094  mov      r9d, r13d
004DC097  seta     r9b
004DC09B  add      r9w, r9w
004DC09F  comiss   xmm9, xmm0
004DC0A3  seta     al
004DC0A6  add      r9w, ax
004DC0AA  mov      eax, r13d
004DC0AD  add      r9w, r9w
004DC0B1  comiss   xmm8, xmm6
004DC0B5  seta     al
004DC0B8  add      r9w, ax
004DC0BC  shl      r9w, 2
004DC0C1  add      r9w, r10w
004DC0C5  add      r9w, r9w
004DC0C9  add      r9w, r8w
004DC0CD  add      r9w, r9w
004DC0D1  add      r9w, cx
004DC0D5  add      r9w, r9w
004DC0D9  ucomiss  xmm4, xmm1
004DC0DC  jp       0x4dc0e6  ; -> 004DC0E6
004DC0DE  mov      r11d, 1
004DC0E4  je       0x4dc0e9  ; -> 004DC0E9
004DC0E6  mov      r11d, r13d
004DC0E9  movaps   xmm6, xmm1
004DC0EC  shufps   xmm6, xmm1, 0x55
004DC0F0  ucomiss  xmm2, xmm6
004DC0F3  jp       0x4dc0fd  ; -> 004DC0FD
004DC0F5  mov      r10d, 1
004DC0FB  je       0x4dc100  ; -> 004DC100
004DC0FD  mov      r10d, r13d
004DC100  movaps   xmm0, xmm1
004DC103  shufps   xmm0, xmm1, 0xaa
004DC107  ucomiss  xmm3, xmm0
004DC10A  jp       0x4dc113  ; -> 004DC113
004DC10C  mov      ecx, 1
004DC111  je       0x4dc116  ; -> 004DC116
004DC113  mov      ecx, r13d
004DC116  comiss   xmm1, xmm4
004DC119  mov      eax, r13d
004DC11C  mov      r8d, r13d
004DC11F  seta     r8b
004DC123  add      r8w, r8w
004DC127  comiss   xmm6, xmm2
004DC12A  seta     al
004DC12D  add      r8w, ax
004DC131  mov      eax, r13d
004DC134  add      r8w, r8w
004DC138  comiss   xmm0, xmm3
004DC13B  seta     al
004DC13E  add      r8w, ax
004DC142  shl      r8w, 2
004DC147  add      r8w, r11w
004DC14B  add      r8w, r8w
004DC14F  add      r8w, r10w
004DC153  add      r8w, r8w
004DC157  add      r8w, cx
004DC15B  add      r8w, r8w
004DC15F  ucomiss  xmm1, xmm13
004DC163  jp       0x4dc16c  ; -> 004DC16C
004DC165  mov      ebx, 1
004DC16A  je       0x4dc16f  ; -> 004DC16F
004DC16C  mov      ebx, r13d
004DC16F  ucomiss  xmm6, xmm9
004DC173  jp       0x4dc17d  ; -> 004DC17D
004DC175  mov      r11d, 1
004DC17B  je       0x4dc180  ; -> 004DC180
004DC17D  mov      r11d, r13d
004DC180  ucomiss  xmm0, xmm8
004DC184  jp       0x4dc18e  ; -> 004DC18E
004DC186  mov      r10d, 1
004DC18C  je       0x4dc191  ; -> 004DC191
004DC18E  mov      r10d, r13d
004DC191  movaps   xmm15, xmmword ptr [rip + 0x439257]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004DC199  mov      eax, r13d
004DC19C  movzx    esi, word ptr [rip + 0x1b88969]  ; -> 02064B0C
004DC1A3  mov      ecx, r13d
004DC1A6  comiss   xmm13, xmm1
004DC1AA  seta     cl
004DC1AD  add      cx, cx
004DC1B0  comiss   xmm9, xmm6
004DC1B4  seta     al
004DC1B7  add      cx, ax
004DC1BA  mov      eax, r13d
004DC1BD  add      cx, cx
004DC1C0  comiss   xmm8, xmm0
004DC1C4  movaps   xmm0, xmm15
004DC1C8  mulps    xmm0, xmm7
004DC1CB  seta     al
004DC1CE  add      cx, ax
004DC1D1  shl      cx, 2
004DC1D5  add      cx, bx
004DC1D8  lea      ebx, [rdi + rsi]
004DC1DB  cvttps2dq xmm7, xmm0
004DC1DF  add      cx, cx
004DC1E2  movzx    edi, bx
004DC1E5  add      cx, r11w
004DC1E9  and      dx, bx
004DC1EC  add      cx, cx
004DC1EF  and      r9w, bx
004DC1F3  add      cx, r10w
004DC1F7  and      r8w, bx
004DC1FB  add      cx, cx
004DC1FE  movaps   xmm0, xmm15
004DC202  mulps    xmm0, xmm1
004DC205  and      di, cx
004DC208  ucomiss  xmm4, xmm5
004DC20B  movups   xmm1, xmmword ptr [rip + 0x1b88a1e]  ; -> 02064C30
004DC212  cvttps2dq xmm11, xmm0
004DC217  movaps   xmm0, xmm10
004DC21B  shufps   xmm0, xmm0, 0
004DC21F  movups   xmmword ptr [rip + 0x1b889ba], xmm7  ; -> 02064BE0
004DC226  movups   xmmword ptr [rip + 0x1b889f2], xmm11  ; -> 02064C20
004DC22E  mulps    xmm1, xmm0
004DC231  jp       0x4dc23a  ; -> 004DC23A
004DC233  mov      ebp, 1
004DC238  je       0x4dc23d  ; -> 004DC23D
004DC23A  mov      ebp, r13d
004DC23D  movaps   xmm6, xmm5
004DC240  shufps   xmm6, xmm5, 0x55
004DC244  ucomiss  xmm2, xmm6
004DC247  jp       0x4dc251  ; -> 004DC251
004DC249  mov      r11d, 1
004DC24F  je       0x4dc254  ; -> 004DC254
004DC251  mov      r11d, r13d
004DC254  movaps   xmm0, xmm5
004DC257  shufps   xmm0, xmm5, 0xaa
004DC25B  ucomiss  xmm3, xmm0
004DC25E  jp       0x4dc267  ; -> 004DC267
004DC260  mov      ecx, 1
004DC265  je       0x4dc26a  ; -> 004DC26A
004DC267  mov      ecx, r13d
004DC26A  comiss   xmm5, xmm4
004DC26D  mov      eax, r13d
004DC270  mov      r10d, r13d
004DC273  seta     r10b
004DC277  add      r10w, r10w
004DC27B  comiss   xmm6, xmm2
004DC27E  seta     al
004DC281  add      r10w, ax
004DC285  mov      eax, r13d
004DC288  add      r10w, r10w
004DC28C  comiss   xmm0, xmm3
004DC28F  seta     al
004DC292  add      r10w, ax
004DC296  movsx    eax, r9w
004DC29A  shl      r10w, 2
004DC29F  or       dx, ax
004DC2A2  add      r10w, bp
004DC2A6  add      r10w, r10w
004DC2AA  add      r10w, r11w
004DC2AE  add      r10w, r10w
004DC2B2  add      r10w, cx
004DC2B6  add      r10w, r10w
004DC2BA  ucomiss  xmm5, xmm13
004DC2BE  mov      word ptr [rip + 0x1b8884a], r10w  ; -> 02064B10
004DC2C6  jp       0x4dc2cf  ; -> 004DC2CF
004DC2C8  mov      ebp, 1
004DC2CD  je       0x4dc2d2  ; -> 004DC2D2
004DC2CF  mov      ebp, r13d
004DC2D2  ucomiss  xmm6, xmm9
004DC2D6  jp       0x4dc2e0  ; -> 004DC2E0
004DC2D8  mov      r9d, 1
004DC2DE  je       0x4dc2e3  ; -> 004DC2E3
004DC2E0  mov      r9d, r13d
004DC2E3  ucomiss  xmm0, xmm8
004DC2E7  jp       0x4dc2f0  ; -> 004DC2F0
004DC2E9  mov      ecx, 1
004DC2EE  je       0x4dc2f3  ; -> 004DC2F3
004DC2F0  mov      ecx, r13d
004DC2F3  comiss   xmm13, xmm5
004DC2F7  mov      eax, r13d
004DC2FA  mov      r11d, r13d
004DC2FD  seta     r11b
004DC301  add      r11w, r11w
004DC305  comiss   xmm9, xmm6
004DC309  seta     al
004DC30C  add      r11w, ax
004DC310  mov      eax, r13d
004DC313  add      r11w, r11w
004DC317  comiss   xmm8, xmm0
004DC31B  seta     al
004DC31E  add      r11w, ax
004DC322  movsx    eax, di
004DC325  shl      r11w, 2
004DC32A  or       r8w, ax
004DC32E  add      r11w, bp
004DC332  add      r11w, r11w
004DC336  add      r11w, r9w
004DC33A  add      r11w, r11w
004DC33E  add      r11w, cx
004DC342  add      r11w, r11w
004DC346  ucomiss  xmm4, xmm1
004DC349  mov      word ptr [rip + 0x1b887c1], r11w  ; -> 02064B12
004DC351  jp       0x4dc35a  ; -> 004DC35A
004DC353  mov      ebp, 1
004DC358  je       0x4dc35d  ; -> 004DC35D
004DC35A  mov      ebp, r13d
004DC35D  movaps   xmm6, xmm1
004DC360  shufps   xmm6, xmm1, 0x55
004DC364  ucomiss  xmm2, xmm6
004DC367  jp       0x4dc370  ; -> 004DC370
004DC369  mov      edi, 1
004DC36E  je       0x4dc373  ; -> 004DC373
004DC370  mov      edi, r13d
004DC373  movaps   xmm0, xmm1
004DC376  shufps   xmm0, xmm1, 0xaa
004DC37A  ucomiss  xmm3, xmm0
004DC37D  jp       0x4dc386  ; -> 004DC386
004DC37F  mov      ecx, 1
004DC384  je       0x4dc389  ; -> 004DC389
004DC386  mov      ecx, r13d
004DC389  comiss   xmm1, xmm4
004DC38C  mov      eax, r13d
004DC38F  mov      r9d, r13d
004DC392  seta     r9b
004DC396  add      r9w, r9w
004DC39A  comiss   xmm6, xmm2
004DC39D  seta     al
004DC3A0  add      r9w, ax
004DC3A4  mov      eax, r13d
004DC3A7  add      r9w, r9w
004DC3AB  comiss   xmm0, xmm3
004DC3AE  seta     al
004DC3B1  add      r9w, ax
004DC3B5  movsx    eax, dx
004DC3B8  shl      r9w, 2
004DC3BD  or       r8w, ax
004DC3C1  add      r9w, bp
004DC3C5  mov      word ptr [rip + 0x1b88a13], r8w  ; -> 02064DE0
004DC3CD  add      r9w, r9w
004DC3D1  add      r9w, di
004DC3D5  add      r9w, r9w
004DC3D9  add      r9w, cx
004DC3DD  add      r9w, r9w
004DC3E1  ucomiss  xmm1, xmm13
004DC3E5  mov      word ptr [rip + 0x1b88727], r9w  ; -> 02064B14
004DC3ED  jp       0x4dc3f6  ; -> 004DC3F6
004DC3EF  mov      ebp, 1
004DC3F4  je       0x4dc3f9  ; -> 004DC3F9
004DC3F6  mov      ebp, r13d
004DC3F9  ucomiss  xmm6, xmm9
004DC3FD  jp       0x4dc406  ; -> 004DC406
004DC3FF  mov      edi, 1
004DC404  je       0x4dc409  ; -> 004DC409
004DC406  mov      edi, r13d
004DC409  ucomiss  xmm0, xmm8
004DC40D  jp       0x4dc416  ; -> 004DC416
004DC40F  mov      edx, 1
004DC414  je       0x4dc419  ; -> 004DC419
004DC416  mov      edx, r13d
004DC419  comiss   xmm13, xmm1
004DC41D  mov      ecx, r13d
004DC420  mov      eax, r13d
004DC423  seta     cl
004DC426  add      cx, cx
004DC429  comiss   xmm9, xmm6
004DC42D  seta     al
004DC430  add      cx, ax
004DC433  mov      eax, r13d
004DC436  add      cx, cx
004DC439  comiss   xmm8, xmm0
004DC43D  movaps   xmm0, xmm15
004DC441  mulps    xmm0, xmm5
004DC444  seta     al
004DC447  and      r10w, bx
004DC44B  add      cx, ax
004DC44E  and      r11w, bx
004DC452  shl      cx, 2
004DC456  and      r9w, bx
004DC45A  add      cx, bp
004DC45D  movsx    eax, r11w
004DC461  or       r10w, ax
004DC465  mov      word ptr [rip + 0x1b8896f], r11w  ; -> 02064DDC
004DC46D  add      cx, cx
004DC470  mov      word ptr [rip + 0x1b88960], r10w  ; -> 02064DD8
004DC478  add      cx, di
004DC47B  cvttps2dq xmm5, xmm0
004DC47F  add      cx, cx
004DC482  add      cx, dx
004DC485  add      cx, cx
004DC488  mov      word ptr [rip + 0x1b88687], cx  ; -> 02064B16
004DC48F  and      bx, cx
004DC492  movsx    eax, bx
004DC495  movaps   xmm0, xmm15
004DC499  or       r9w, ax
004DC49D  mulps    xmm0, xmm1
004DC4A0  movsx    eax, r10w
004DC4A4  movsx    r10d, word ptr [rip + 0x1b88908]  ; -> 02064DB4
004DC4AC  or       r9w, ax
004DC4B0  mov      ecx, r10d
004DC4B3  mov      word ptr [rip + 0x1b8892e], bx  ; -> 02064DE8
004DC4BA  shl      ecx, 4
004DC4BD  cvttps2dq xmm6, xmm0
004DC4C1  movsxd   rax, ecx
004DC4C4  mov      word ptr [rip + 0x1b88918], r9w  ; -> 02064DE4
004DC4CC  movups   xmm0, xmmword ptr [rip + 0x1b8876d]  ; -> 02064C40
004DC4D3  movups   xmmword ptr [rip + 0x1b88716], xmm5  ; -> 02064BF0
004DC4DA  cvttps2dq xmm1, xmm0
004DC4DE  movups   xmm0, xmmword ptr [rip + 0x1b8876b]  ; -> 02064C50
004DC4E5  movups   xmmword ptr [rax + r14], xmm1
004DC4EA  lea      eax, [rcx + 0x10]
004DC4ED  movsxd   r11, eax
004DC4F0  lea      eax, [r10 + 2]
004DC4F4  shl      eax, 4
004DC4F7  movsxd   rbp, eax
004DC4FA  lea      eax, [r10 + 3]
004DC4FE  shl      eax, 4
004DC501  movsxd   rbx, eax
004DC504  lea      eax, [r10 + 4]
004DC508  shl      eax, 4
004DC50B  movsxd   rcx, eax
004DC50E  lea      eax, [r10 + 5]
004DC512  cvttps2dq xmm2, xmm0
004DC516  shl      eax, 4
004DC519  movups   xmm0, xmmword ptr [rip + 0x1b88740]  ; -> 02064C60
004DC520  movups   xmmword ptr [r11 + r14], xmm7
004DC525  cvttps2dq xmm3, xmm0
004DC529  movups   xmm0, xmmword ptr [rip + 0x1b88740]  ; -> 02064C70
004DC530  movups   xmmword ptr [r14 + rbp], xmm2
004DC535  movups   xmmword ptr [rbx + r14], xmm11
004DC53A  movups   xmmword ptr [rcx + r14], xmm3
004DC53F  movsxd   rcx, eax
004DC542  lea      eax, [r10 + 6]
004DC546  cvttps2dq xmm4, xmm0
004DC54A  shl      eax, 4
004DC54D  movups   xmmword ptr [rcx + r14], xmm5
004DC552  movups   xmmword ptr [rip + 0x1b886d7], xmm6  ; -> 02064C30
004DC559  movups   xmmword ptr [rip + 0x1b886e0], xmm1  ; -> 02064C40
004DC560  movups   xmmword ptr [rip + 0x1b886e9], xmm2  ; -> 02064C50
004DC567  movups   xmmword ptr [rip + 0x1b886f2], xmm3  ; -> 02064C60
004DC56E  movups   xmmword ptr [rip + 0x1b886fb], xmm4  ; -> 02064C70
004DC575  movsxd   r14, eax
004DC578  lea      rdi, [rip + 0x1b888b1]  ; -> 02064E30
004DC57F  lea      eax, [r10 + 7]
004DC583  shl      eax, 4
004DC586  movsxd   rdx, eax
004DC589  cmp      r8w, si
004DC58D  movups   xmmword ptr [r14 + rdi], xmm4
004DC592  lea      r8, [rip + 0x1b88897]  ; -> 02064E30
004DC599  movups   xmmword ptr [rdx + rdi], xmm6
004DC59D  movzx    edi, word ptr [rip + 0x1b88830]  ; -> 02064DD4
004DC5A4  je       0x4dc5b8  ; -> 004DC5B8
004DC5A6  mov      dword ptr [r11 + r8 + 0xc], r13d
004DC5AB  mov      dword ptr [r8 + rbp + 0xc], r13d
004DC5B0  mov      dword ptr [rbx + r8 + 0xc], r13d
004DC5B5  movzx    eax, di
004DC5B8  cmp      r9w, si
004DC5BC  je       0x4dc5de  ; -> 004DC5DE
004DC5BE  movzx    eax, di
004DC5C1  mov      dword ptr [rdx + r8 + 0xc], eax
004DC5C6  mov      dword ptr [rcx + r8 + 0xc], r13d
004DC5CB  mov      dword ptr [r14 + r8 + 0xc], r13d
004DC5D0  lea      r14, [rip + 0x1b88859]  ; -> 02064E30
004DC5D7  mov      dword ptr [rdx + r14 + 0xc], r13d
004DC5DC  jmp      0x4dc5e5  ; -> 004DC5E5
004DC5DE  lea      r14, [rip + 0x1b8884b]  ; -> 02064E30
004DC5E5  movzx    eax, word ptr [rip + 0x1b887cc]  ; -> 02064DB8
004DC5EC  add      r10w, 8
004DC5F1  add      ax, 2
004DC5F5  mov      word ptr [rip + 0x1b887b7], r10w  ; -> 02064DB4
004DC5FD  cmp      ax, word ptr [rip + 0x1b887b8]  ; -> 02064DBC
004DC604  mov      word ptr [rip + 0x1b887ad], ax  ; -> 02064DB8
004DC60B  jne      0x4dc62f  ; -> 004DC62F
004DC60D  mov      rdx, r15
004DC610  mov      rcx, r12
004DC613  call     0x4db270  ; -> 004DB270 fn
004DC618  movzx    eax, word ptr [rip + 0x1b88799]  ; -> 02064DB8
004DC61F  movzx    esi, word ptr [rip + 0x1b884e6]  ; -> 02064B0C
004DC626  movss    xmm14, dword ptr [rip + 0x192620d]  ; -> 01E0283C [f32 1]
004DC62F  movzx    r9d, word ptr [rip + 0x1b88789]  ; -> 02064DC0
004DC637  test     r9w, r9w
004DC63B  jle      0x4dc64a  ; -> 004DC64A
004DC63D  movzx    r8d, word ptr [rip + 0x1b8877f]  ; -> 02064DC4
004DC645  jmp      0x4db5c6  ; -> 004DB5C6
004DC64A  cmp      ax, si
004DC64D  je       0x4dc65a  ; -> 004DC65A
004DC64F  mov      rdx, r15
004DC652  mov      rcx, r12
004DC655  call     0x4db270  ; -> 004DB270 fn
004DC65A  movaps   xmm14, xmmword ptr [rsp + 0x40]
004DC660  lea      r11, [rsp + 0xd0]
004DC668  mov      rbx, qword ptr [r11 + 0x48]
004DC66C  movaps   xmm6, xmmword ptr [r11 - 0x10]
004DC671  movaps   xmm7, xmmword ptr [r11 - 0x20]
004DC676  movaps   xmm8, xmmword ptr [r11 - 0x30]
004DC67B  movaps   xmm9, xmmword ptr [r11 - 0x40]
004DC680  movaps   xmm10, xmmword ptr [r11 - 0x50]
004DC685  movaps   xmm11, xmmword ptr [r11 - 0x60]
004DC68A  movaps   xmm12, xmmword ptr [r11 - 0x70]
004DC68F  movaps   xmm13, xmmword ptr [r11 - 0x80]
004DC694  movaps   xmm15, xmmword ptr [rsp + 0x30]
004DC69A  mov      rsp, r11
004DC69D  pop      r15
004DC69F  pop      r14
004DC6A1  pop      r13
004DC6A3  pop      r12
004DC6A5  pop      rdi
004DC6A6  pop      rsi
004DC6A7  pop      rbp
004DC6A8  ret      
```

## 004DDDF0 (5479 B, extent 004DDDF0-004DF357)

Page context: "acy-PS2-GS/the-vif1-vu1-layer.md)'s template census decodes; §2.4b there reads the rest of this chain and gives the map — type ''h'' installs '004DF440' and '004E0F70', ''i'' installs '004DCC00' and '004DDDF0', '0xA3' installs '004DB350', '0xA6' and '0xA8' share '004DA8A0', and ''j'' installs '004D7BF0'. **The copied template carries the MPG descriptor verbatim**, which is how the program reaches the packet at all: the builder only re-p"

```
004DDDF0  mov      rax, rsp
004DDDF3  mov      qword ptr [rax + 0x10], rdx
004DDDF7  mov      qword ptr [rax + 8], rcx
004DDDFB  push     rbx
004DDDFC  push     rbp
004DDDFD  push     rsi
004DDDFE  push     rdi
004DDDFF  push     r12
004DDE01  push     r13
004DDE03  push     r14
004DDE05  sub      rsp, 0xe0
004DDE0C  movsx    r10d, word ptr [rip + 0x1b86cf8]  ; -> 02064B0C
004DDE14  lea      r14, [rip + 0x1b87015]  ; -> 02064E30
004DDE1B  movaps   xmmword ptr [rax - 0x48], xmm6
004DDE1F  mov      rbx, rcx
004DDE22  movaps   xmmword ptr [rax - 0x58], xmm7
004DDE26  mov      r11, rdx
004DDE29  movaps   xmmword ptr [rax - 0x68], xmm8
004DDE2E  movaps   xmmword ptr [rax - 0x78], xmm9
004DDE33  movaps   xmmword ptr [rax - 0x88], xmm10
004DDE3B  movaps   xmmword ptr [rax - 0x98], xmm11
004DDE43  lea      eax, [r10 + 0x81]
004DDE4A  shl      eax, 4
004DDE4D  movsxd   r8, eax
004DDE50  lea      eax, [r10 + 0x80]
004DDE57  shl      eax, 4
004DDE5A  movsxd   rdx, eax
004DDE5D  movaps   xmmword ptr [rsp + 0x70], xmm12
004DDE63  movups   xmm1, xmmword ptr [r8 + r14]
004DDE68  xor      r8d, r8d
004DDE6B  movaps   xmmword ptr [rsp + 0x60], xmm13
004DDE71  movzx    eax, word ptr [rdx + r14 + 8]
004DDE77  movups   xmm0, xmmword ptr [rdx + r14]
004DDE7C  mov      word ptr [rip + 0x1b86f59], ax  ; -> 02064DDC
004DDE83  movaps   xmmword ptr [rsp + 0x50], xmm14
004DDE89  movaps   xmmword ptr [rsp + 0x40], xmm15
004DDE8F  mov      rdx, r11
004DDE92  lea      eax, [r10 + 3]
004DDE96  shl      eax, 4
004DDE99  movsxd   rcx, eax
004DDE9C  mov      eax, 0x83
004DDEA1  add      r10w, ax
004DDEA5  movsx    eax, r10w
004DDEA9  cvtdq2ps xmm1, xmm1
004DDEAC  shl      eax, 4
004DDEAF  mov      word ptr [rip + 0x1b86f1d], r10w  ; -> 02064DD4
004DDEB7  movups   xmmword ptr [rip + 0x1b86d12], xmm0  ; -> 02064BD0
004DDEBE  movups   xmm0, xmmword ptr [rcx + r14]
004DDEC3  movsxd   rcx, eax
004DDEC6  add      rcx, r14
004DDEC9  movups   xmmword ptr [rip + 0x1b86d20], xmm0  ; -> 02064BF0
004DDED0  movups   xmmword ptr [rip + 0x1b86ce9], xmm1  ; -> 02064BC0
004DDED7  call     rbx
004DDED9  movss    xmm1, dword ptr [rip + 0x192494f]  ; -> 01E02830 [u32 0x00000000]
004DDEE1  mov      edi, 0x320
004DDEE6  movzx    ebx, word ptr [rip + 0x1b86c1f]  ; -> 02064B0C
004DDEED  movaps   xmm2, xmm1
004DDEF0  movss    xmm0, dword ptr [rip + 0x1b86d00]  ; -> 02064BF8
004DDEF8  add      edi, ebx
004DDEFA  movss    xmm15, dword ptr [rip + 0x1b86cd9]  ; -> 02064BDC
004DDF03  addss    xmm0, xmm1
004DDF07  movss    xmm12, dword ptr [rip + 0x1924928]  ; -> 01E02838 [u32 0x00000000]
004DDF10  addss    xmm2, xmm15
004DDF15  movss    xmm13, dword ptr [rip + 0x192491e]  ; -> 01E0283C [f32 1]
004DDF1E  movss    xmm11, dword ptr [rip + 0x192490d]  ; -> 01E02834 [u32 0x00000000]
004DDF27  addss    xmm12, xmm13
004DDF2C  movss    xmm14, dword ptr [rip + 0x42242b]  ; -> 00900360 [u32 0x7F7FFFFF]
004DDF35  mulss    xmm11, xmm1
004DDF3A  mov      word ptr [rip + 0x1b86e6f], di  ; -> 02064DB0
004DDF41  inc      di
004DDF44  ucomiss  xmm2, dword ptr [rip + 0x423a39]  ; -> 00901984 [u32 0x00000000]
004DDF4B  mov      word ptr [rip + 0x1b86e62], di  ; -> 02064DB4
004DDF52  mov      word ptr [rip + 0x1b86e5f], bx  ; -> 02064DB8
004DDF59  mov      word ptr [rip + 0x1b86e70], bx  ; -> 02064DD0
004DDF60  movups   xmm1, xmmword ptr [rip + 0x1b86c59]  ; -> 02064BC0
004DDF67  subss    xmm12, xmm15
004DDF6C  movss    dword ptr [rip + 0x1b86c7c], xmm0  ; -> 02064BF0
004DDF74  mulps    xmm1, xmmword ptr [rip + 0x844795]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004DDF7B  movss    xmm0, dword ptr [rip + 0x3e7bb1]  ; -> 008C5B34 [f32 0.0078125]
004DDF83  movss    dword ptr [rsp + 0x20], xmm2
004DDF89  movss    dword ptr [rip + 0x1b86c56], xmm12  ; -> 02064BE8
004DDF92  movups   xmmword ptr [rip + 0x1b86c27], xmm1  ; -> 02064BC0
004DDF99  movss    dword ptr [rip + 0x1b86c3f], xmm2  ; -> 02064BE0
004DDFA1  movss    dword ptr [rip + 0x1b86c4a], xmm11  ; -> 02064BF4
004DDFAA  movss    dword ptr [rip + 0x1b86b52], xmm0  ; -> 02064B04
004DDFB2  jp       0x4ddfbc  ; -> 004DDFBC
004DDFB4  jne      0x4ddfbc  ; -> 004DDFBC
004DDFB6  movaps   xmm0, xmm14
004DDFBA  jmp      0x4ddfc4  ; -> 004DDFC4
004DDFBC  movaps   xmm0, xmm13
004DDFC0  divss    xmm0, xmm2
004DDFC4  movss    xmm10, dword ptr [rip + 0x1b86bf3]  ; -> 02064BC0
004DDFCD  movss    xmm8, dword ptr [rip + 0x1b86bf2]  ; -> 02064BC8
004DDFD6  movss    xmm9, dword ptr [rip + 0x1b86be5]  ; -> 02064BC4
004DDFDF  movss    xmm7, dword ptr [rip + 0x1b86be5]  ; -> 02064BCC
004DDFE7  movss    dword ptr [rip + 0x1b86b11], xmm0  ; -> 02064B00
004DDFEF  movss    dword ptr [rsp + 0x138], xmm0
004DDFF8  movsx    edx, bx
004DDFFB  lea      eax, [rdx + 4]
004DDFFE  shl      eax, 4
004DE001  movsxd   rcx, eax
004DE004  lea      eax, [rdx + 5]
004DE007  shl      eax, 4
004DE00A  movups   xmm0, xmmword ptr [rcx + r14]
004DE00F  movsxd   rcx, eax
004DE012  lea      eax, [rdx + 6]
004DE015  shl      eax, 4
004DE018  movups   xmmword ptr [rip + 0x1b86b11], xmm0  ; -> 02064B30
004DE01F  movups   xmm2, xmmword ptr [rcx + r14]
004DE024  movsxd   rcx, eax
004DE027  lea      eax, [rdx + 7]
004DE02A  movss    xmm1, dword ptr [rip + 0x1b86b02]  ; -> 02064B34
004DE032  movss    dword ptr [rip + 0x1b86af6], xmm0  ; -> 02064B30
004DE03A  mulss    xmm0, xmm10
004DE03F  shl      eax, 4
004DE042  movups   xmm3, xmmword ptr [rcx + r14]
004DE047  movsxd   rcx, eax
004DE04A  lea      eax, [rdx + 8]
004DE04D  movss    dword ptr [rip + 0x1b86adb], xmm0  ; -> 02064B30
004DE055  movss    xmm0, dword ptr [rip + 0x1b86adb]  ; -> 02064B38
004DE05D  mulss    xmm0, xmm8
004DE062  shl      eax, 4
004DE065  movups   xmm6, xmmword ptr [rcx + r14]
004DE06A  movsxd   rcx, eax
004DE06D  lea      eax, [rdx + 9]
004DE070  movss    dword ptr [rip + 0x1b86ac0], xmm0  ; -> 02064B38
004DE078  movups   xmmword ptr [rip + 0x1b86ac1], xmm2  ; -> 02064B40
004DE07F  shl      eax, 4
004DE082  movss    xmm0, dword ptr [rip + 0x1b86aba]  ; -> 02064B44
004DE08A  movups   xmm4, xmmword ptr [rcx + r14]
004DE08F  movsxd   rcx, eax
004DE092  lea      eax, [rdx + 0xa]
004DE095  mulss    xmm0, xmm9
004DE09A  shl      eax, 4
004DE09D  movups   xmmword ptr [rip + 0x1b86aac], xmm3  ; -> 02064B50
004DE0A4  movups   xmm5, xmmword ptr [rcx + r14]
004DE0A9  movsxd   rcx, eax
004DE0AC  movss    dword ptr [rip + 0x1b86a90], xmm0  ; -> 02064B44
004DE0B4  movss    xmm0, dword ptr [rip + 0x1b86a90]  ; -> 02064B4C
004DE0BC  mulss    xmm0, xmm7
004DE0C0  mulss    xmm1, xmm9
004DE0C5  movss    dword ptr [rip + 0x1b86a7f], xmm0  ; -> 02064B4C
004DE0CD  movss    xmm0, dword ptr [rip + 0x1b86a7f]  ; -> 02064B54
004DE0D5  mulss    xmm0, xmm9
004DE0DA  movss    dword ptr [rip + 0x1b86a52], xmm1  ; -> 02064B34
004DE0E2  movss    xmm1, dword ptr [rip + 0x1b86a52]  ; -> 02064B3C
004DE0EA  movss    dword ptr [rip + 0x1b86a62], xmm0  ; -> 02064B54
004DE0F2  movss    xmm0, dword ptr [rip + 0x1b86a62]  ; -> 02064B5C
004DE0FA  mulss    xmm1, xmm7
004DE0FE  mulss    xmm0, xmm7
004DE102  movss    dword ptr [rip + 0x1b86a32], xmm1  ; -> 02064B3C
004DE10A  movss    xmm1, dword ptr [rip + 0x1b86a36]  ; -> 02064B48
004DE112  movss    dword ptr [rip + 0x1b86a42], xmm0  ; -> 02064B5C
004DE11A  movups   xmm0, xmmword ptr [rcx + r14]
004DE11F  mulss    xmm1, xmm8
004DE124  movups   xmmword ptr [rsp + 0x28], xmm0
004DE129  movups   xmmword ptr [rip + 0x1b86a60], xmm0  ; -> 02064B90
004DE130  movss    dword ptr [rip + 0x1b86a10], xmm1  ; -> 02064B48
004DE138  movaps   xmm0, xmm6
004DE13B  movss    xmm1, dword ptr [rip + 0x1b86a15]  ; -> 02064B58
004DE143  mulss    xmm0, xmm10
004DE148  mulss    xmm2, xmm10
004DE14D  mulss    xmm3, xmm10
004DE152  mulss    xmm1, xmm8
004DE157  movups   xmmword ptr [rip + 0x1b86a02], xmm6  ; -> 02064B60
004DE15E  movss    dword ptr [rip + 0x1b869fa], xmm6  ; -> 02064B60
004DE166  movss    dword ptr [rip + 0x1b869f2], xmm0  ; -> 02064B60
004DE16E  movss    dword ptr [rip + 0x1b869ca], xmm2  ; -> 02064B40
004DE176  movss    dword ptr [rip + 0x1b869d2], xmm3  ; -> 02064B50
004DE17E  movss    dword ptr [rip + 0x1b869d2], xmm1  ; -> 02064B58
004DE186  movups   xmmword ptr [rip + 0x1b869e3], xmm4  ; -> 02064B70
004DE18D  movups   xmmword ptr [rip + 0x1b869ec], xmm5  ; -> 02064B80
004DE194  movss    xmm0, dword ptr [rip + 0x1b869cc]  ; -> 02064B68
004DE19C  lea      eax, [rdx + 0xb]
004DE19F  movss    xmm1, dword ptr [rip + 0x1b869bd]  ; -> 02064B64
004DE1A7  mulss    xmm0, xmm8
004DE1AC  shl      eax, 4
004DE1AF  mulss    xmm1, xmm9
004DE1B4  movsxd   rcx, eax
004DE1B7  lea      eax, [rdx + 0xc]
004DE1BA  movss    dword ptr [rip + 0x1b869a6], xmm0  ; -> 02064B68
004DE1C2  movss    xmm0, dword ptr [rip + 0x1b869aa]  ; -> 02064B74
004DE1CA  mulss    xmm0, xmm9
004DE1CF  shl      eax, 4
004DE1D2  movups   xmm3, xmmword ptr [rcx + r14]
004DE1D7  add      dx, bx
004DE1DA  movsxd   rcx, eax
004DE1DD  movss    dword ptr [rip + 0x1b8697f], xmm1  ; -> 02064B64
004DE1E5  movss    xmm1, dword ptr [rip + 0x1b8697f]  ; -> 02064B6C
004DE1ED  movss    dword ptr [rip + 0x1b8697f], xmm0  ; -> 02064B74
004DE1F5  movss    xmm0, dword ptr [rip + 0x1b8697f]  ; -> 02064B7C
004DE1FD  movups   xmm2, xmmword ptr [rcx + r14]
004DE202  mov      word ptr [rip + 0x1b86bb3], bx  ; -> 02064DBC
004DE209  mulss    xmm0, xmm7
004DE20D  mov      word ptr [rip + 0x1b86bb0], dx  ; -> 02064DC4
004DE214  mulss    xmm1, xmm7
004DE218  movss    dword ptr [rip + 0x1b8695c], xmm0  ; -> 02064B7C
004DE220  movss    xmm0, dword ptr [rip + 0x1b8695c]  ; -> 02064B84
004DE228  mulss    xmm0, xmm9
004DE22D  movss    dword ptr [rip + 0x1b86937], xmm1  ; -> 02064B6C
004DE235  movss    xmm1, dword ptr [rip + 0x1b8693b]  ; -> 02064B78
004DE23D  movss    dword ptr [rip + 0x1b8693f], xmm0  ; -> 02064B84
004DE245  movss    xmm0, dword ptr [rip + 0x1b8693f]  ; -> 02064B8C
004DE24D  mulss    xmm0, xmm7
004DE251  mulss    xmm1, xmm8
004DE256  movss    dword ptr [rip + 0x1b8692e], xmm0  ; -> 02064B8C
004DE25E  movss    xmm0, dword ptr [rip + 0x1b8692e]  ; -> 02064B94
004DE266  mulss    xmm0, xmm9
004DE26B  movups   xmmword ptr [rip + 0x1b8692e], xmm3  ; -> 02064BA0
004DE272  movss    dword ptr [rip + 0x1b8691a], xmm0  ; -> 02064B94
004DE27A  movss    xmm0, dword ptr [rip + 0x1b8691a]  ; -> 02064B9C
004DE282  mulss    xmm0, xmm7
004DE286  movss    dword ptr [rip + 0x1b868ea], xmm1  ; -> 02064B78
004DE28E  movss    xmm1, dword ptr [rip + 0x1b868f2]  ; -> 02064B88
004DE296  movss    dword ptr [rip + 0x1b868fe], xmm0  ; -> 02064B9C
004DE29E  movss    xmm0, dword ptr [rip + 0x1b868fe]  ; -> 02064BA4
004DE2A6  mulss    xmm0, xmm9
004DE2AB  movups   xmmword ptr [rip + 0x1b868fe], xmm2  ; -> 02064BB0
004DE2B2  movss    dword ptr [rip + 0x1b868ea], xmm0  ; -> 02064BA4
004DE2BA  movss    xmm0, dword ptr [rip + 0x1b868ea]  ; -> 02064BAC
004DE2C2  mulss    xmm0, xmm7
004DE2C6  mulss    xmm1, xmm8
004DE2CB  movss    dword ptr [rip + 0x1b868d9], xmm0  ; -> 02064BAC
004DE2D3  movss    xmm0, dword ptr [rip + 0x1b868d9]  ; -> 02064BB4
004DE2DB  movss    dword ptr [rip + 0x1b868a5], xmm1  ; -> 02064B88
004DE2E3  movss    xmm1, dword ptr [rip + 0x1b868ad]  ; -> 02064B98
004DE2EB  mulss    xmm0, xmm9
004DE2F0  mulss    xmm1, xmm8
004DE2F5  movss    dword ptr [rip + 0x1b868b7], xmm0  ; -> 02064BB4
004DE2FD  movss    xmm0, dword ptr [rip + 0x1b868b7]  ; -> 02064BBC
004DE305  movss    dword ptr [rip + 0x1b8688b], xmm1  ; -> 02064B98
004DE30D  movss    xmm1, dword ptr [rip + 0x1b86893]  ; -> 02064BA8
004DE315  mulss    xmm4, xmm10
004DE31A  mulss    xmm0, xmm7
004DE31E  mulss    xmm1, xmm8
004DE323  movss    dword ptr [rip + 0x1b86845], xmm4  ; -> 02064B70
004DE32B  movups   xmm4, xmmword ptr [rsp + 0x28]
004DE330  movss    dword ptr [rip + 0x1b86884], xmm0  ; -> 02064BBC
004DE338  movss    xmm0, dword ptr [rip + 0x19244f4]  ; -> 01E02834 [u32 0x00000000]
004DE340  addss    xmm0, dword ptr [rsp + 0x138]
004DE349  movss    dword ptr [rip + 0x1b86857], xmm1  ; -> 02064BA8
004DE351  movss    xmm1, dword ptr [rip + 0x1b8685f]  ; -> 02064BB8
004DE359  mulss    xmm5, xmm10
004DE35E  mulss    xmm4, xmm10
004DE363  mulss    xmm3, xmm10
004DE368  mulss    xmm2, xmm10
004DE36D  mulss    xmm1, xmm8
004DE372  movss    dword ptr [rip + 0x1b8686a], xmm0  ; -> 02064BE4
004DE37A  movss    dword ptr [rip + 0x1b867fe], xmm5  ; -> 02064B80
004DE382  movss    dword ptr [rip + 0x1b86806], xmm4  ; -> 02064B90
004DE38A  movss    dword ptr [rip + 0x1b8680e], xmm3  ; -> 02064BA0
004DE392  movss    dword ptr [rip + 0x1b86816], xmm2  ; -> 02064BB0
004DE39A  movss    dword ptr [rip + 0x1b86816], xmm1  ; -> 02064BB8
004DE3A2  xorps    xmm6, xmm6
004DE3A5  ucomiss  xmm0, xmm6
004DE3A8  jp       0x4de3f5  ; -> 004DE3F5
004DE3AA  jne      0x4de3f5  ; -> 004DE3F5
004DE3AC  call     0x22cc40  ; -> 0022CC40 fn
004DE3B1  movss    xmm2, dword ptr [rip + 0x1b86827]  ; -> 02064BE0
004DE3B9  movss    xmm4, dword ptr [rip + 0x1b867cf]  ; -> 02064B90
004DE3C1  movzx    ebx, word ptr [rip + 0x1b86744]  ; -> 02064B0C
004DE3C8  movss    xmm11, dword ptr [rip + 0x1b86823]  ; -> 02064BF4
004DE3D1  movss    xmm13, dword ptr [rip + 0x1924462]  ; -> 01E0283C [f32 1]
004DE3DA  movss    xmm12, dword ptr [rip + 0x1b86805]  ; -> 02064BE8
004DE3E3  movzx    edi, word ptr [rip + 0x1b869ca]  ; -> 02064DB4
004DE3EA  movss    xmm15, dword ptr [rip + 0x1b867e9]  ; -> 02064BDC
004DE3F3  jmp      0x4de3fb  ; -> 004DE3FB
004DE3F5  movss    xmm2, dword ptr [rsp + 0x20]
004DE3FB  comiss   xmm6, dword ptr [rip + 0x1b867e2]  ; -> 02064BE4
004DE402  jbe      0x4de44b  ; -> 004DE44B
004DE404  call     0x22cc30  ; -> 0022CC30 fn
004DE409  movss    xmm2, dword ptr [rip + 0x1b867cf]  ; -> 02064BE0
004DE411  movss    xmm4, dword ptr [rip + 0x1b86777]  ; -> 02064B90
004DE419  movzx    ebx, word ptr [rip + 0x1b866ec]  ; -> 02064B0C
004DE420  movss    xmm11, dword ptr [rip + 0x1b867cb]  ; -> 02064BF4
004DE429  movss    xmm13, dword ptr [rip + 0x192440a]  ; -> 01E0283C [f32 1]
004DE432  movss    xmm12, dword ptr [rip + 0x1b867ad]  ; -> 02064BE8
004DE43B  movzx    edi, word ptr [rip + 0x1b86972]  ; -> 02064DB4
004DE442  movss    xmm15, dword ptr [rip + 0x1b86791]  ; -> 02064BDC
004DE44B  ucomiss  xmm12, xmm6
004DE44F  jp       0x4de453  ; -> 004DE453
004DE451  je       0x4de45c  ; -> 004DE45C
004DE453  movaps   xmm14, xmm13
004DE457  divss    xmm14, xmm12
004DE45C  movsx    r8d, bx
004DE460  mov      eax, r8d
004DE463  movss    dword ptr [rip + 0x1b86694], xmm14  ; -> 02064B00
004DE46C  shl      eax, 4
004DE46F  movsxd   rcx, eax
004DE472  movzx    eax, word ptr [rcx + r14 + 0xc]
004DE478  mov      word ptr [rip + 0x1b86949], ax  ; -> 02064DC8
004DE47F  lea      eax, [rbx + r8]
004DE483  mov      word ptr [rip + 0x1b86942], ax  ; -> 02064DCC
004DE48A  lea      eax, [r8 + 0x80]
004DE491  shl      eax, 4
004DE494  movsxd   rcx, eax
004DE497  lea      eax, [r8 + 0x82]
004DE49E  shl      eax, 4
004DE4A1  movzx    edx, word ptr [rcx + r14 + 4]
004DE4A7  movsxd   rcx, eax
004DE4AA  lea      eax, [r8 + 3]
004DE4AE  shl      eax, 4
004DE4B1  movups   xmm0, xmmword ptr [rcx + r14]
004DE4B6  movsxd   rcx, eax
004DE4B9  movups   xmmword ptr [rip + 0x1b86850], xmm0  ; -> 02064D10
004DE4C0  movups   xmm0, xmmword ptr [rcx + r14]
004DE4C5  movups   xmmword ptr [rip + 0x1b86784], xmm0  ; -> 02064C50
004DE4CC  cmp      dx, bx
004DE4CF  je       0x4de4e9  ; -> 004DE4E9
004DE4D1  movss    xmm0, dword ptr [rip + 0x1b8683f]  ; -> 02064D18
004DE4D9  mulss    xmm0, dword ptr [rip + 0x1b8676f]  ; -> 02064C50
004DE4E1  movss    dword ptr [rip + 0x1b8682f], xmm0  ; -> 02064D18
004DE4E9  movss    xmm9, dword ptr [rip + 0x3e764e]  ; -> 008C5B40 [f32 255]
004DE4F2  lea      eax, [r8 + 2]
004DE4F6  movups   xmm12, xmmword ptr [rip + 0x1b86772]  ; -> 02064C70
004DE4FE  shl      eax, 4
004DE501  movups   xmm1, xmmword ptr [rip + 0x1b86788]  ; -> 02064C90
004DE508  movsxd   rcx, eax
004DE50B  mulss    xmm14, xmm13
004DE510  mov      qword ptr [rsp + 0x130], r15
004DE518  movups   xmm13, xmmword ptr [rip + 0x1b86760]  ; -> 02064C80
004DE520  movzx    eax, word ptr [rcx + r14]
004DE525  add      ax, 2
004DE529  movss    dword ptr [rip + 0x1b866ba], xmm14  ; -> 02064BEC
004DE532  nop      dword ptr [rax]
004DE536  nop      word ptr [rax + rax]
004DE540  dec      ax
004DE543  ucomiss  xmm15, xmm11
004DE547  mov      word ptr [rip + 0x1b86886], ax  ; -> 02064DD4
004DE54E  jp       0x4de559  ; -> 004DE559
004DE550  jne      0x4de559  ; -> 004DE559
004DE552  mov      eax, 1
004DE557  jmp      0x4de55b  ; -> 004DE55B
004DE559  xor      eax, eax
004DE55B  xor      r8d, r8d
004DE55E  movsx    edx, di
004DE561  comiss   xmm11, xmm15
004DE565  seta     r8b
004DE569  shl      r8w, 4
004DE56E  add      r8w, ax
004DE572  lea      eax, [rdx + 1]
004DE575  shl      eax, 4
004DE578  movsxd   rcx, eax
004DE57B  lea      eax, [rdx + 7]
004DE57E  shl      eax, 4
004DE581  mov      word ptr [rip + 0x1b86587], r8w  ; -> 02064B10
004DE589  movups   xmmword ptr [rcx + r14], xmm12
004DE58E  movsxd   rcx, eax
004DE591  lea      eax, [rdx + 0xd]
004DE594  shl      eax, 4
004DE597  movups   xmmword ptr [rcx + r14], xmm13
004DE59C  movsxd   rcx, eax
004DE59F  lea      eax, [rbx + 0x10]
004DE5A2  and      ax, r8w
004DE5A6  mov      word ptr [rip + 0x1b86837], ax  ; -> 02064DE4
004DE5AD  movups   xmmword ptr [rcx + r14], xmm1
004DE5B2  cmp      ax, bx
004DE5B5  jne      0x4de865  ; -> 004DE865
004DE5BB  movss    xmm0, dword ptr [rip + 0x1b86621]  ; -> 02064BE4
004DE5C3  movss    xmm1, dword ptr [rip + 0x1b86595]  ; -> 02064B60
004DE5CB  subss    xmm1, dword ptr [rip + 0x1b8655d]  ; -> 02064B30
004DE5D3  mulss    xmm0, xmm11
004DE5D8  movss    dword ptr [rip + 0x1b86664], xmm0  ; -> 02064C44
004DE5E0  movss    xmm0, dword ptr [rip + 0x1b8657c]  ; -> 02064B64
004DE5E8  subss    xmm0, dword ptr [rip + 0x1b86544]  ; -> 02064B34
004DE5F0  movss    dword ptr [rip + 0x1b86678], xmm1  ; -> 02064C70
004DE5F8  movss    xmm1, dword ptr [rip + 0x1b86568]  ; -> 02064B68
004DE600  subss    xmm1, dword ptr [rip + 0x1b86530]  ; -> 02064B38
004DE608  movss    dword ptr [rip + 0x1b86664], xmm0  ; -> 02064C74
004DE610  movss    xmm0, dword ptr [rip + 0x1b86554]  ; -> 02064B6C
004DE618  subss    xmm0, dword ptr [rip + 0x1b8651c]  ; -> 02064B3C
004DE620  movss    dword ptr [rip + 0x1b86650], xmm1  ; -> 02064C78
004DE628  movss    dword ptr [rip + 0x1b8664c], xmm0  ; -> 02064C7C
004DE630  call     0x22cc20  ; -> 0022CC20 fn
004DE635  movups   xmm0, xmmword ptr [rip + 0x1b86674]  ; -> 02064CB0
004DE63C  movsx    eax, word ptr [rip + 0x1b86771]  ; -> 02064DB4
004DE643  movss    xmm1, dword ptr [rip + 0x1b86525]  ; -> 02064B70
004DE64B  add      eax, 2
004DE64E  subss    xmm1, dword ptr [rip + 0x1b864ea]  ; -> 02064B40
004DE656  shl      eax, 4
004DE659  movsxd   rcx, eax
004DE65C  movss    dword ptr [rip + 0x1b8661c], xmm1  ; -> 02064C80
004DE664  movss    xmm1, dword ptr [rip + 0x1b8650c]  ; -> 02064B78
004DE66C  subss    xmm1, dword ptr [rip + 0x1b864d4]  ; -> 02064B48
004DE674  movups   xmmword ptr [rcx + r14], xmm0
004DE679  movss    xmm0, dword ptr [rip + 0x1b864f3]  ; -> 02064B74
004DE681  subss    xmm0, dword ptr [rip + 0x1b864bb]  ; -> 02064B44
004DE689  movss    dword ptr [rip + 0x1b865f7], xmm1  ; -> 02064C88
004DE691  movss    dword ptr [rip + 0x1b865eb], xmm0  ; -> 02064C84
004DE699  movss    xmm0, dword ptr [rip + 0x1b864db]  ; -> 02064B7C
004DE6A1  subss    xmm0, dword ptr [rip + 0x1b864a3]  ; -> 02064B4C
004DE6A9  movss    dword ptr [rip + 0x1b865db], xmm0  ; -> 02064C8C
004DE6B1  call     0x22cc20  ; -> 0022CC20 fn
004DE6B6  movups   xmm0, xmmword ptr [rip + 0x1b86603]  ; -> 02064CC0
004DE6BD  movsx    eax, word ptr [rip + 0x1b866f0]  ; -> 02064DB4
004DE6C4  movss    xmm1, dword ptr [rip + 0x1b864b4]  ; -> 02064B80
004DE6CC  add      eax, 8
004DE6CF  subss    xmm1, dword ptr [rip + 0x1b86479]  ; -> 02064B50
004DE6D7  shl      eax, 4
004DE6DA  movsxd   rcx, eax
004DE6DD  movss    dword ptr [rip + 0x1b865ab], xmm1  ; -> 02064C90
004DE6E5  movss    xmm1, dword ptr [rip + 0x1b8649b]  ; -> 02064B88
004DE6ED  subss    xmm1, dword ptr [rip + 0x1b86463]  ; -> 02064B58
004DE6F5  movups   xmmword ptr [rcx + r14], xmm0
004DE6FA  movss    xmm0, dword ptr [rip + 0x1b86482]  ; -> 02064B84
004DE702  subss    xmm0, dword ptr [rip + 0x1b8644a]  ; -> 02064B54
004DE70A  movss    dword ptr [rip + 0x1b86586], xmm1  ; -> 02064C98
004DE712  movss    dword ptr [rip + 0x1b8657a], xmm0  ; -> 02064C94
004DE71A  movss    xmm0, dword ptr [rip + 0x1b8646a]  ; -> 02064B8C
004DE722  subss    xmm0, dword ptr [rip + 0x1b86432]  ; -> 02064B5C
004DE72A  movss    dword ptr [rip + 0x1b8656a], xmm0  ; -> 02064C9C
004DE732  call     0x22cc20  ; -> 0022CC20 fn
004DE737  movss    xmm1, dword ptr [rip + 0x1b86505]  ; -> 02064C44
004DE73F  movsx    edi, word ptr [rip + 0x1b8666e]  ; -> 02064DB4
004DE746  movups   xmm0, xmmword ptr [rip + 0x1b86583]  ; -> 02064CD0
004DE74D  mov      r11d, edi
004DE750  movss    xmm3, dword ptr [rip + 0x1b8651c]  ; -> 02064C74
004DE758  movss    xmm2, dword ptr [rip + 0x1b86510]  ; -> 02064C70
004DE760  lea      eax, [rdi + 0xe]
004DE763  movss    xmm4, dword ptr [rip + 0x1b8650d]  ; -> 02064C78
004DE76B  movss    xmm5, dword ptr [rip + 0x1b86509]  ; -> 02064C7C
004DE773  movss    xmm7, dword ptr [rip + 0x1b86509]  ; -> 02064C84
004DE77B  movss    xmm6, dword ptr [rip + 0x1b864fd]  ; -> 02064C80
004DE783  movss    xmm8, dword ptr [rip + 0x1b864fc]  ; -> 02064C88
004DE78C  movss    xmm10, dword ptr [rip + 0x1b864f7]  ; -> 02064C8C
004DE795  movss    xmm12, dword ptr [rip + 0x1b864f6]  ; -> 02064C94
004DE79E  movss    xmm11, dword ptr [rip + 0x1b864e9]  ; -> 02064C90
004DE7A7  shl      eax, 4
004DE7AA  movsxd   r15, eax
004DE7AD  mulss    xmm3, xmm1
004DE7B1  mulss    xmm2, xmm1
004DE7B5  movups   xmmword ptr [r15 + r14], xmm0
004DE7BA  mulss    xmm4, xmm1
004DE7BE  mulss    xmm5, xmm1
004DE7C2  mulss    xmm7, xmm1
004DE7C6  mulss    xmm6, xmm1
004DE7CA  mulss    xmm8, xmm1
004DE7CF  mulss    xmm10, xmm1
004DE7D4  mulss    xmm12, xmm1
004DE7D9  movss    xmm13, dword ptr [rip + 0x1b864b6]  ; -> 02064C98
004DE7E2  movss    xmm14, dword ptr [rip + 0x1b864b1]  ; -> 02064C9C
004DE7EB  addss    xmm2, dword ptr [rip + 0x1b8633d]  ; -> 02064B30
004DE7F3  addss    xmm3, dword ptr [rip + 0x1b86339]  ; -> 02064B34
004DE7FB  addss    xmm4, dword ptr [rip + 0x1b86335]  ; -> 02064B38
004DE803  addss    xmm5, dword ptr [rip + 0x1b86331]  ; -> 02064B3C
004DE80B  addss    xmm6, dword ptr [rip + 0x1b8632d]  ; -> 02064B40
004DE813  addss    xmm7, dword ptr [rip + 0x1b86329]  ; -> 02064B44
004DE81B  addss    xmm8, dword ptr [rip + 0x1b86324]  ; -> 02064B48
004DE824  addss    xmm10, dword ptr [rip + 0x1b8631f]  ; -> 02064B4C
004DE82D  addss    xmm12, dword ptr [rip + 0x1b8631e]  ; -> 02064B54
004DE836  mulss    xmm13, xmm1
004DE83B  mulss    xmm14, xmm1
004DE840  addss    xmm13, dword ptr [rip + 0x1b8630f]  ; -> 02064B58
004DE849  mulss    xmm11, xmm1
004DE84E  addss    xmm14, dword ptr [rip + 0x1b86305]  ; -> 02064B5C
004DE857  addss    xmm11, dword ptr [rip + 0x1b862f0]  ; -> 02064B50
004DE860  jmp      0x4deb00  ; -> 004DEB00
004DE865  movss    xmm0, dword ptr [rip + 0x1b86327]  ; -> 02064B94
004DE86D  subss    xmm11, xmm2
004DE872  subss    xmm0, dword ptr [rip + 0x1b862ea]  ; -> 02064B64
004DE87A  movss    xmm1, dword ptr [rip + 0x1b86316]  ; -> 02064B98
004DE882  subss    xmm4, dword ptr [rip + 0x1b862d6]  ; -> 02064B60
004DE88A  subss    xmm1, dword ptr [rip + 0x1b862d6]  ; -> 02064B68
004DE892  mulss    xmm11, xmm14
004DE897  movss    dword ptr [rip + 0x1b863d5], xmm0  ; -> 02064C74
004DE89F  movss    xmm0, dword ptr [rip + 0x1b862f5]  ; -> 02064B9C
004DE8A7  subss    xmm0, dword ptr [rip + 0x1b862bd]  ; -> 02064B6C
004DE8AF  movss    dword ptr [rip + 0x1b8638c], xmm11  ; -> 02064C44
004DE8B8  movss    dword ptr [rip + 0x1b863b0], xmm4  ; -> 02064C70
004DE8C0  movss    dword ptr [rip + 0x1b863b0], xmm1  ; -> 02064C78
004DE8C8  movss    dword ptr [rip + 0x1b863ac], xmm0  ; -> 02064C7C
004DE8D0  call     0x22cc20  ; -> 0022CC20 fn
004DE8D5  movups   xmm0, xmmword ptr [rip + 0x1b863d4]  ; -> 02064CB0
004DE8DC  movsx    eax, word ptr [rip + 0x1b864d1]  ; -> 02064DB4
004DE8E3  movss    xmm1, dword ptr [rip + 0x1b862b5]  ; -> 02064BA0
004DE8EB  add      eax, 2
004DE8EE  subss    xmm1, dword ptr [rip + 0x1b8627a]  ; -> 02064B70
004DE8F6  shl      eax, 4
004DE8F9  movsxd   rcx, eax
004DE8FC  movss    dword ptr [rip + 0x1b8637c], xmm1  ; -> 02064C80
004DE904  movss    xmm1, dword ptr [rip + 0x1b8629c]  ; -> 02064BA8
004DE90C  subss    xmm1, dword ptr [rip + 0x1b86264]  ; -> 02064B78
004DE914  movups   xmmword ptr [rcx + r14], xmm0
004DE919  movss    xmm0, dword ptr [rip + 0x1b86283]  ; -> 02064BA4
004DE921  subss    xmm0, dword ptr [rip + 0x1b8624b]  ; -> 02064B74
004DE929  movss    dword ptr [rip + 0x1b86357], xmm1  ; -> 02064C88
004DE931  movss    dword ptr [rip + 0x1b8634b], xmm0  ; -> 02064C84
004DE939  movss    xmm0, dword ptr [rip + 0x1b8626b]  ; -> 02064BAC
004DE941  subss    xmm0, dword ptr [rip + 0x1b86233]  ; -> 02064B7C
004DE949  movss    dword ptr [rip + 0x1b8633b], xmm0  ; -> 02064C8C
004DE951  call     0x22cc20  ; -> 0022CC20 fn
004DE956  movups   xmm0, xmmword ptr [rip + 0x1b86363]  ; -> 02064CC0
004DE95D  movsx    eax, word ptr [rip + 0x1b86450]  ; -> 02064DB4
004DE964  movss    xmm1, dword ptr [rip + 0x1b86244]  ; -> 02064BB0
004DE96C  add      eax, 8
004DE96F  subss    xmm1, dword ptr [rip + 0x1b86209]  ; -> 02064B80
004DE977  shl      eax, 4
004DE97A  movsxd   rcx, eax
004DE97D  movss    dword ptr [rip + 0x1b8630b], xmm1  ; -> 02064C90
004DE985  movss    xmm1, dword ptr [rip + 0x1b8622b]  ; -> 02064BB8
004DE98D  subss    xmm1, dword ptr [rip + 0x1b861f3]  ; -> 02064B88
004DE995  movups   xmmword ptr [rcx + r14], xmm0
004DE99A  movss    xmm0, dword ptr [rip + 0x1b86212]  ; -> 02064BB4
004DE9A2  subss    xmm0, dword ptr [rip + 0x1b861da]  ; -> 02064B84
004DE9AA  movss    dword ptr [rip + 0x1b862e6], xmm1  ; -> 02064C98
004DE9B2  movss    dword ptr [rip + 0x1b862da], xmm0  ; -> 02064C94
004DE9BA  movss    xmm0, dword ptr [rip + 0x1b861fa]  ; -> 02064BBC
004DE9C2  subss    xmm0, dword ptr [rip + 0x1b861c2]  ; -> 02064B8C
004DE9CA  movss    dword ptr [rip + 0x1b862ca], xmm0  ; -> 02064C9C
004DE9D2  call     0x22cc20  ; -> 0022CC20 fn
004DE9D7  movss    xmm1, dword ptr [rip + 0x1b86265]  ; -> 02064C44
004DE9DF  movsx    edi, word ptr [rip + 0x1b863ce]  ; -> 02064DB4
004DE9E6  movups   xmm0, xmmword ptr [rip + 0x1b862e3]  ; -> 02064CD0
004DE9ED  mov      r11d, edi
004DE9F0  movss    xmm3, dword ptr [rip + 0x1b8627c]  ; -> 02064C74
004DE9F8  movss    xmm2, dword ptr [rip + 0x1b86270]  ; -> 02064C70
004DEA00  lea      eax, [rdi + 0xe]
004DEA03  movss    xmm4, dword ptr [rip + 0x1b8626d]  ; -> 02064C78
004DEA0B  movss    xmm5, dword ptr [rip + 0x1b86269]  ; -> 02064C7C
004DEA13  movss    xmm7, dword ptr [rip + 0x1b86269]  ; -> 02064C84
004DEA1B  movss    xmm6, dword ptr [rip + 0x1b8625d]  ; -> 02064C80
004DEA23  movss    xmm8, dword ptr [rip + 0x1b8625c]  ; -> 02064C88
004DEA2C  movss    xmm10, dword ptr [rip + 0x1b86257]  ; -> 02064C8C
004DEA35  movss    xmm12, dword ptr [rip + 0x1b86256]  ; -> 02064C94
004DEA3E  movss    xmm11, dword ptr [rip + 0x1b86249]  ; -> 02064C90
004DEA47  shl      eax, 4
004DEA4A  movsxd   r15, eax
004DEA4D  mulss    xmm3, xmm1
004DEA51  mulss    xmm2, xmm1
004DEA55  movups   xmmword ptr [r15 + r14], xmm0
004DEA5A  mulss    xmm4, xmm1
004DEA5E  mulss    xmm5, xmm1
004DEA62  mulss    xmm7, xmm1
004DEA66  mulss    xmm6, xmm1
004DEA6A  mulss    xmm8, xmm1
004DEA6F  mulss    xmm10, xmm1
004DEA74  mulss    xmm12, xmm1
004DEA79  mulss    xmm11, xmm1
004DEA7E  movss    xmm13, dword ptr [rip + 0x1b86211]  ; -> 02064C98
004DEA87  movss    xmm14, dword ptr [rip + 0x1b8620c]  ; -> 02064C9C
004DEA90  addss    xmm2, dword ptr [rip + 0x1b860c8]  ; -> 02064B60
004DEA98  addss    xmm3, dword ptr [rip + 0x1b860c4]  ; -> 02064B64
004DEAA0  addss    xmm4, dword ptr [rip + 0x1b860c0]  ; -> 02064B68
004DEAA8  addss    xmm5, dword ptr [rip + 0x1b860bc]  ; -> 02064B6C
004DEAB0  addss    xmm6, dword ptr [rip + 0x1b860b8]  ; -> 02064B70
004DEAB8  addss    xmm7, dword ptr [rip + 0x1b860b4]  ; -> 02064B74
004DEAC0  addss    xmm8, dword ptr [rip + 0x1b860af]  ; -> 02064B78
004DEAC9  addss    xmm10, dword ptr [rip + 0x1b860aa]  ; -> 02064B7C
004DEAD2  addss    xmm11, dword ptr [rip + 0x1b860a5]  ; -> 02064B80
004DEADB  addss    xmm12, dword ptr [rip + 0x1b860a0]  ; -> 02064B84
004DEAE4  mulss    xmm13, xmm1
004DEAE9  mulss    xmm14, xmm1
004DEAEE  addss    xmm13, dword ptr [rip + 0x1b86091]  ; -> 02064B88
004DEAF7  addss    xmm14, dword ptr [rip + 0x1b8608c]  ; -> 02064B8C
004DEB00  movups   xmm0, xmmword ptr [rip + 0x1b86109]  ; -> 02064C10
004DEB07  mov      eax, edi
004DEB09  movss    dword ptr [rip + 0x1b8618a], xmm14  ; -> 02064C9C
004DEB12  shl      eax, 4
004DEB15  movsxd   rcx, eax
004DEB18  lea      eax, [rdi + 6]
004DEB1B  shl      eax, 4
004DEB1E  movss    dword ptr [rip + 0x1b86171], xmm13  ; -> 02064C98
004DEB27  movss    dword ptr [rip + 0x1b86164], xmm12  ; -> 02064C94
004DEB30  movups   xmmword ptr [rcx + r14], xmm0
004DEB35  movsxd   rcx, eax
004DEB38  lea      eax, [rdi + 0xc]
004DEB3B  movups   xmm0, xmmword ptr [rip + 0x1b860de]  ; -> 02064C20
004DEB42  shl      eax, 4
004DEB45  comiss   xmm9, xmm2
004DEB49  movups   xmmword ptr [rcx + r14], xmm0
004DEB4E  movsxd   rcx, eax
004DEB51  movups   xmm0, xmmword ptr [rip + 0x1b860d8]  ; -> 02064C30
004DEB58  movss    dword ptr [rip + 0x1b8612f], xmm11  ; -> 02064C90
004DEB61  movups   xmmword ptr [rcx + r14], xmm0
004DEB66  movss    dword ptr [rip + 0x1b8611d], xmm10  ; -> 02064C8C
004DEB6F  movss    dword ptr [rip + 0x1b86110], xmm8  ; -> 02064C88
004DEB78  movss    dword ptr [rip + 0x1b86104], xmm7  ; -> 02064C84
004DEB80  movss    dword ptr [rip + 0x1b860f8], xmm6  ; -> 02064C80
004DEB88  movss    dword ptr [rip + 0x1b860ec], xmm5  ; -> 02064C7C
004DEB90  movss    dword ptr [rip + 0x1b860e0], xmm4  ; -> 02064C78
004DEB98  movss    dword ptr [rip + 0x1b860d4], xmm3  ; -> 02064C74
004DEBA0  movss    dword ptr [rip + 0x1b860c8], xmm2  ; -> 02064C70
004DEBA8  ja       0x4debb4  ; -> 004DEBB4
004DEBAA  mov      dword ptr [rip + 0x1b860bc], 0x437f0000  ; -> 02064C70
004DEBB4  comiss   xmm9, xmm3
004DEBB8  ja       0x4debc4  ; -> 004DEBC4
004DEBBA  mov      dword ptr [rip + 0x1b860b0], 0x437f0000  ; -> 02064C74
004DEBC4  comiss   xmm9, xmm4
004DEBC8  ja       0x4debd4  ; -> 004DEBD4
004DEBCA  mov      dword ptr [rip + 0x1b860a4], 0x437f0000  ; -> 02064C78
004DEBD4  comiss   xmm9, xmm5
004DEBD8  ja       0x4debe4  ; -> 004DEBE4
004DEBDA  mov      dword ptr [rip + 0x1b86098], 0x437f0000  ; -> 02064C7C
004DEBE4  comiss   xmm9, xmm6
004DEBE8  ja       0x4debf4  ; -> 004DEBF4
004DEBEA  mov      dword ptr [rip + 0x1b8608c], 0x437f0000  ; -> 02064C80
004DEBF4  comiss   xmm9, xmm7
004DEBF8  ja       0x4dec04  ; -> 004DEC04
004DEBFA  mov      dword ptr [rip + 0x1b86080], 0x437f0000  ; -> 02064C84
004DEC04  comiss   xmm9, xmm8
004DEC08  ja       0x4dec14  ; -> 004DEC14
004DEC0A  mov      dword ptr [rip + 0x1b86074], 0x437f0000  ; -> 02064C88
004DEC14  comiss   xmm9, xmm10
004DEC18  ja       0x4dec24  ; -> 004DEC24
004DEC1A  mov      dword ptr [rip + 0x1b86068], 0x437f0000  ; -> 02064C8C
004DEC24  comiss   xmm9, xmm11
004DEC28  ja       0x4dec34  ; -> 004DEC34
004DEC2A  mov      dword ptr [rip + 0x1b8605c], 0x437f0000  ; -> 02064C90
004DEC34  comiss   xmm9, xmm12
004DEC38  ja       0x4dec44  ; -> 004DEC44
004DEC3A  mov      dword ptr [rip + 0x1b86050], 0x437f0000  ; -> 02064C94
004DEC44  comiss   xmm9, xmm13
004DEC48  ja       0x4dec54  ; -> 004DEC54
004DEC4A  mov      dword ptr [rip + 0x1b86044], 0x437f0000  ; -> 02064C98
004DEC54  comiss   xmm9, xmm14
004DEC58  ja       0x4dec64  ; -> 004DEC64
004DEC5A  mov      dword ptr [rip + 0x1b86038], 0x437f0000  ; -> 02064C9C
004DEC64  movss    xmm2, dword ptr [rip + 0x180d018]  ; -> 01CEBC84 [f32 16]
004DEC6C  movsx    esi, word ptr [rip + 0x1b86149]  ; -> 02064DBC
004DEC73  movups   xmm1, xmmword ptr [rip + 0x1b86006]  ; -> 02064C80
004DEC7A  mov      dword ptr [rip + 0x1b85e80], 0x3f000000  ; -> 02064B04
004DEC84  movups   xmm0, xmmword ptr [rip + 0x1b85fe5]  ; -> 02064C70
004DEC8B  lea      eax, [rsi + 0x100]
004DEC91  shl      eax, 4
004DEC94  cvttps2dq xmm0, xmm0
004DEC98  movsxd   rcx, eax
004DEC9B  lea      eax, [rsi + 0x180]
004DECA1  shl      eax, 4
004DECA4  movsxd   r8, eax
004DECA7  lea      eax, [rsi + 0x200]
004DECAD  shl      eax, 4
004DECB0  movups   xmm5, xmmword ptr [rcx + r14]
004DECB5  movsxd   rcx, eax
004DECB8  movzx    ebp, word ptr [r8 + r14 + 0xc]
004DECBE  movups   xmmword ptr [rip + 0x1b85fab], xmm0  ; -> 02064C70
004DECC5  mov      word ptr [rip + 0x1b860f4], bp  ; -> 02064DC0
004DECCC  movups   xmm6, xmmword ptr [rcx + r14]
004DECD1  cvttps2dq xmm0, xmm1
004DECD5  movups   xmm1, xmmword ptr [rip + 0x1b85fb4]  ; -> 02064C90
004DECDC  movups   xmmword ptr [rip + 0x1b85f9d], xmm0  ; -> 02064C80
004DECE3  movups   xmm0, xmmword ptr [r8 + r14]
004DECE8  movsx    r14d, word ptr [rip + 0x1b860d4]  ; -> 02064DC4
004DECF0  movaps   xmm7, xmm5
004DECF3  movaps   xmm8, xmm6
004DECF7  movups   xmmword ptr [rip + 0x1b85fc2], xmm0  ; -> 02064CC0
004DECFE  or       r14w, bp
004DED02  movss    xmm12, dword ptr [rip + 0x1b85fb5]  ; -> 02064CC0
004DED0B  movaps   xmm14, xmm5
004DED0F  movss    xmm13, dword ptr [rip + 0x1b85fac]  ; -> 02064CC4
004DED18  movaps   xmm15, xmm6
004DED1C  cvttps2dq xmm0, xmm1
004DED20  mov      word ptr [rip + 0x1b8609c], r14w  ; -> 02064DC4
004DED28  movaps   xmm1, xmm5
004DED2B  shufps   xmm7, xmm5, 0x55
004DED2F  movups   xmmword ptr [rip + 0x1b85f5a], xmm0  ; -> 02064C90
004DED36  shufps   xmm1, xmm5, 0xaa
004DED3A  movaps   xmm0, xmm5
004DED3D  mulss    xmm0, xmm2
004DED41  mulss    xmm1, xmm2
004DED45  cvttss2si r12d, xmm0
004DED4A  movaps   xmm0, xmm7
004DED4D  shufps   xmm8, xmm6, 0x55
004DED52  mulss    xmm0, xmm2
004DED56  mov      dword ptr [rip + 0x1b85f83], r12d  ; -> 02064CE0
004DED5D  cvttss2si eax, xmm1
004DED61  movss    xmm1, dword ptr [rip + 0x1b85f5f]  ; -> 02064CC8
004DED69  cvttss2si r13d, xmm0
004DED6E  mov      dword ptr [rip + 0x1b85f74], eax  ; -> 02064CE8
004DED74  mulss    xmm1, xmm2
004DED78  movaps   xmm0, xmm12
004DED7C  mov      dword ptr [rip + 0x1b85f61], r13d  ; -> 02064CE4
004DED83  mulss    xmm0, xmm2
004DED87  shufps   xmm14, xmm5, 0xff
004DED8C  movaps   xmm10, xmm14
004DED90  shufps   xmm15, xmm6, 0xff
004DED95  cvttss2si eax, xmm0
004DED99  movaps   xmm0, xmm13
004DED9D  addss    xmm10, xmm15
004DEDA2  mulss    xmm0, xmm2
004DEDA6  mov      dword ptr [rip + 0x1b85f44], eax  ; -> 02064CF0
004DEDAC  movups   xmmword ptr [rip + 0x1b85efd], xmm5  ; -> 02064CB0
004DEDB3  cvttss2si eax, xmm0
004DEDB7  movaps   xmm0, xmm6
004DEDBA  mov      dword ptr [rip + 0x1b85f34], eax  ; -> 02064CF4
004DEDC0  cvttss2si eax, xmm1
004DEDC4  mulss    xmm0, xmm2
004DEDC8  movaps   xmm1, xmm6
004DEDCB  mov      dword ptr [rip + 0x1b85f27], eax  ; -> 02064CF8
004DEDD1  shufps   xmm1, xmm6, 0xaa
004DEDD5  mulss    xmm1, xmm2
004DEDD9  cvttss2si eax, xmm0
004DEDDD  movaps   xmm0, xmm8
004DEDE1  mov      dword ptr [rip + 0x1b85f19], eax  ; -> 02064D00
004DEDE7  mulss    xmm0, xmm2
004DEDEB  movups   xmmword ptr [rip + 0x1b85ede], xmm6  ; -> 02064CD0
004DEDF2  cvttss2si eax, xmm0
004DEDF6  mov      dword ptr [rip + 0x1b85f08], eax  ; -> 02064D04
004DEDFC  cvttss2si eax, xmm1
004DEE00  mulss    xmm10, dword ptr [rip + 0x180cd67]  ; -> 01CEBB70 [f32 0.5]
004DEE09  lea      rdx, [rip + 0x1b86020]  ; -> 02064E30
004DEE10  movzx    ebx, word ptr [rip + 0x1b85cf5]  ; -> 02064B0C
004DEE17  movss    xmm11, dword ptr [rip + 0x1b85dd4]  ; -> 02064BF4
004DEE20  mov      dword ptr [rip + 0x1b85ee2], eax  ; -> 02064D08
004DEE26  lea      eax, [r11 + 5]
004DEE2A  shl      eax, 4
004DEE2D  movsxd   r8, eax
004DEE30  lea      eax, [r11 + 0xb]
004DEE34  shl      eax, 4
004DEE37  movsxd   r10, eax
004DEE3A  lea      eax, [r11 + 0x11]
004DEE3E  shl      eax, 4
004DEE41  movsxd   r9, eax
004DEE44  lea      eax, [r11 + 4]
004DEE48  shl      eax, 4
004DEE4B  cmp      word ptr [rip + 0x1b85f8a], bx  ; -> 02064DDC
004DEE52  movss    dword ptr [rip + 0x1b85e71], xmm10  ; -> 02064CCC
004DEE5B  movsxd   rcx, eax
004DEE5E  jne      0x4defb9  ; -> 004DEFB9
004DEE64  movss    xmm6, dword ptr [rip + 0x1b85ea8]  ; -> 02064D14
004DEE6C  lea      eax, [r11 + 0xa]
004DEE70  addss    xmm6, dword ptr [rip + 0x19239bc]  ; -> 01E02834 [u32 0x00000000]
004DEE78  movss    xmm0, dword ptr [rip + 0x1b85e9c]  ; -> 02064D1C
004DEE80  movss    xmm4, dword ptr [rip + 0x1b85e88]  ; -> 02064D10
004DEE88  movaps   xmm1, xmm0
004DEE8B  mulss    xmm1, dword ptr [rip + 0x1b85dc9]  ; -> 02064C5C
004DEE93  shl      eax, 4
004DEE96  addss    xmm4, dword ptr [rip + 0x1923992]  ; -> 01E02830 [u32 0x00000000]
004DEE9E  movss    xmm2, dword ptr [rip + 0x1b85e72]  ; -> 02064D18
004DEEA6  movaps   xmm8, xmm6
004DEEAA  movups   xmm12, xmmword ptr [rip + 0x1b85dbe]  ; -> 02064C70
004DEEB2  movups   xmm13, xmmword ptr [rip + 0x1b85dc6]  ; -> 02064C80
004DEEBA  addss    xmm8, xmm0
004DEEBF  mulss    xmm2, xmm11
004DEEC4  movups   xmm0, xmmword ptr [rip + 0x1b85e15]  ; -> 02064CE0
004DEECB  movaps   xmm3, xmm4
004DEECE  movss    dword ptr [rip + 0x1b85d76], xmm1  ; -> 02064C4C
004DEED6  movups   xmmword ptr [r8 + rdx], xmm0
004DEEDB  movups   xmm0, xmmword ptr [rip + 0x1b85e0e]  ; -> 02064CF0
004DEEE2  movaps   xmm5, xmm4
004DEEE5  movss    dword ptr [rip + 0x1b85d57], xmm2  ; -> 02064C44
004DEEED  movups   xmmword ptr [r10 + rdx], xmm0
004DEEF2  movups   xmm0, xmmword ptr [rip + 0x1b85e07]  ; -> 02064D00
004DEEF9  movaps   xmm7, xmm6
004DEEFC  addss    xmm4, xmm2
004DEF00  addss    xmm7, xmm1
004DEF04  movss    xmm1, dword ptr [rip + 0x192392c]  ; -> 01E02838 [u32 0x00000000]
004DEF0C  addss    xmm14, xmm1
004DEF11  addss    xmm10, xmm1
004DEF16  addss    xmm15, xmm1
004DEF1B  movups   xmm1, xmmword ptr [rip + 0x1b85d6e]  ; -> 02064C90
004DEF22  movups   xmmword ptr [r9 + rdx], xmm0
004DEF27  movups   xmmword ptr [rcx + rdx], xmm12
004DEF2C  movsxd   rcx, eax
004DEF2F  lea      eax, [r11 + 0x10]
004DEF33  addss    xmm3, xmm2
004DEF37  shl      eax, 4
004DEF3A  addss    xmm5, xmm2
004DEF3E  mulss    xmm6, xmm14
004DEF43  movups   xmmword ptr [rcx + rdx], xmm13
004DEF48  movsxd   rcx, eax
004DEF4B  mulss    xmm4, xmm14
004DEF50  mulss    xmm7, xmm10
004DEF55  mulss    xmm3, xmm10
004DEF5A  mulss    xmm8, xmm15
004DEF5F  mulss    xmm5, xmm15
004DEF64  movups   xmmword ptr [rcx + rdx], xmm1
004DEF68  movss    dword ptr [rip + 0x1b85ca7], xmm14  ; -> 02064C18
004DEF71  movss    dword ptr [rip + 0x1b85cae], xmm10  ; -> 02064C28
004DEF7A  movss    dword ptr [rip + 0x1b85cb5], xmm15  ; -> 02064C38
004DEF83  movss    dword ptr [rip + 0x1b85c89], xmm6  ; -> 02064C14
004DEF8B  movss    dword ptr [rip + 0x1b85c7d], xmm4  ; -> 02064C10
004DEF93  movss    dword ptr [rip + 0x1b85c89], xmm7  ; -> 02064C24
004DEF9B  movss    dword ptr [rip + 0x1b85c7d], xmm3  ; -> 02064C20
004DEFA3  movss    dword ptr [rip + 0x1b85c88], xmm8  ; -> 02064C34
004DEFAC  movss    dword ptr [rip + 0x1b85c7c], xmm5  ; -> 02064C30
004DEFB4  jmp      0x4df138  ; -> 004DF138
004DEFB9  movss    xmm10, dword ptr [rip + 0x3e6b6e]  ; -> 008C5B30 [f32 0.001953125]
004DEFC2  lea      eax, [r11 + 0xa]
004DEFC6  movss    xmm0, dword ptr [rip + 0x43664a]  ; -> 00915618 [f32 1792]
004DEFCE  movss    xmm1, dword ptr [rip + 0x436646]  ; -> 0091561C [f32 1824]
004DEFD6  subss    xmm12, xmm0
004DEFDB  movss    xmm4, dword ptr [rip + 0x1923855]  ; -> 01E02838 [u32 0x00000000]
004DEFE3  subss    xmm5, xmm0
004DEFE7  addss    xmm4, dword ptr [rip + 0x192384d]  ; -> 01E0283C [f32 1]
004DEFEF  subss    xmm6, xmm0
004DEFF3  shl      eax, 4
004DEFF6  movups   xmm0, xmmword ptr [rip + 0x1b85ce3]  ; -> 02064CE0
004DEFFD  mov      dword ptr [rip + 0x1b85afd], 0x3b000000  ; -> 02064B04
004DF007  subss    xmm13, xmm1
004DF00C  mulss    xmm12, xmm10
004DF011  movups   xmmword ptr [r8 + rdx], xmm0
004DF016  movups   xmm0, xmmword ptr [rip + 0x1b85cd3]  ; -> 02064CF0
004DF01D  subss    xmm7, xmm1
004DF021  mulss    xmm13, xmm10
004DF026  movups   xmmword ptr [r10 + rdx], xmm0
004DF02B  movups   xmm0, xmmword ptr [rip + 0x1b85cce]  ; -> 02064D00
004DF032  subss    xmm8, xmm1
004DF037  mulss    xmm5, xmm10
004DF03C  movss    xmm1, dword ptr [rip + 0x1b85ccc]  ; -> 02064D10
004DF044  movaps   xmm3, xmm4
004DF047  movups   xmmword ptr [r9 + rdx], xmm0
004DF04C  movups   xmm0, xmmword ptr [rip + 0x1b85c1d]  ; -> 02064C70
004DF053  movaps   xmm2, xmm4
004DF056  mulss    xmm6, xmm10
004DF05B  movups   xmmword ptr [rcx + rdx], xmm0
004DF05F  movsxd   rcx, eax
004DF062  lea      eax, [r11 + 0x10]
004DF066  movups   xmm0, xmmword ptr [rip + 0x1b85c13]  ; -> 02064C80
004DF06D  shl      eax, 4
004DF070  addss    xmm12, xmm1
004DF075  mulss    xmm7, xmm10
004DF07A  movups   xmmword ptr [rcx + rdx], xmm0
004DF07E  movsxd   rcx, eax
004DF081  movups   xmm0, xmmword ptr [rip + 0x1b85c08]  ; -> 02064C90
004DF088  mulss    xmm12, xmm3
004DF08D  addss    xmm5, xmm1
004DF091  mulss    xmm8, xmm10
004DF096  addss    xmm6, xmm1
004DF09A  movups   xmm1, xmmword ptr [rip + 0x1b85bef]  ; -> 02064C90
004DF0A1  mulss    xmm5, xmm4
004DF0A5  mulss    xmm6, xmm2
004DF0A9  movups   xmmword ptr [rcx + rdx], xmm0
004DF0AD  movss    xmm0, dword ptr [rip + 0x1b85c5f]  ; -> 02064D14
004DF0B5  addss    xmm13, xmm0
004DF0BA  movss    dword ptr [rip + 0x1b85b5d], xmm12  ; -> 02064C20
004DF0C3  movups   xmm12, xmmword ptr [rip + 0x1b85ba5]  ; -> 02064C70
004DF0CB  addss    xmm7, xmm0
004DF0CF  movss    dword ptr [rip + 0x1b85b39], xmm5  ; -> 02064C10
004DF0D7  addss    xmm8, xmm0
004DF0DC  movss    dword ptr [rip + 0x1b85b4c], xmm6  ; -> 02064C30
004DF0E4  mulss    xmm13, xmm3
004DF0E9  mulss    xmm3, xmm3
004DF0ED  mulss    xmm7, xmm4
004DF0F1  mulss    xmm8, xmm2
004DF0F6  mulss    xmm4, xmm4
004DF0FA  mulss    xmm2, xmm2
004DF0FE  movss    dword ptr [rip + 0x1b85b1d], xmm13  ; -> 02064C24
004DF107  movups   xmm13, xmmword ptr [rip + 0x1b85b71]  ; -> 02064C80
004DF10F  movss    dword ptr [rip + 0x1b85b01], xmm4  ; -> 02064C18
004DF117  movss    dword ptr [rip + 0x1b85b09], xmm3  ; -> 02064C28
004DF11F  movss    dword ptr [rip + 0x1b85b11], xmm2  ; -> 02064C38
004DF127  movss    dword ptr [rip + 0x1b85ae5], xmm7  ; -> 02064C14
004DF12F  movss    dword ptr [rip + 0x1b85afc], xmm8  ; -> 02064C34
004DF138  movzx    edx, word ptr [rip + 0x1b85c89]  ; -> 02064DC8
004DF13F  lea      rax, [rip + 0x1b85cea]  ; -> 02064E30
004DF146  mov      dword ptr [r8 + rax + 0xc], edx
004DF14B  movzx    r8d, word ptr [rip + 0x1b85c79]  ; -> 02064DCC
004DF153  mov      dword ptr [r10 + rax + 0xc], r8d
004DF158  lea      r10, [rip + 0x1b85cd1]  ; -> 02064E30
004DF15F  mov      dword ptr [r9 + r10 + 0xc], r8d
004DF164  lea      eax, [r11 + 2]
004DF168  shl      eax, 4
004DF16B  movsxd   rcx, eax
004DF16E  lea      eax, [r11 + 8]
004DF172  shl      eax, 4
004DF175  mov      dword ptr [rcx + r10 + 0xc], edx
004DF17A  movsxd   rcx, eax
004DF17D  mov      dword ptr [rcx + r10 + 0xc], r8d
004DF182  mov      dword ptr [r15 + r10 + 0xc], r8d
004DF187  mov      eax, dword ptr [rip + 0x1b85b5b]  ; -> 02064CE8
004DF18D  cmp      bx, r14w
004DF191  mov      dword ptr [rip + 0x1b85b21], eax  ; -> 02064CB8
004DF197  lea      r14, [rip + 0x1b85c92]  ; -> 02064E30
004DF19E  mov      eax, dword ptr [rip + 0x1b85b4c]  ; -> 02064CF0
004DF1A4  mov      dword ptr [rip + 0x1b85b16], eax  ; -> 02064CC0
004DF1AA  mov      eax, dword ptr [rip + 0x1b85b44]  ; -> 02064CF4
004DF1B0  mov      dword ptr [rip + 0x1b85b0e], eax  ; -> 02064CC4
004DF1B6  mov      eax, dword ptr [rip + 0x1b85b3c]  ; -> 02064CF8
004DF1BC  mov      dword ptr [rip + 0x1b85b06], eax  ; -> 02064CC8
004DF1C2  mov      eax, dword ptr [rip + 0x1b85b38]  ; -> 02064D00
004DF1C8  mov      dword ptr [rip + 0x1b85b02], eax  ; -> 02064CD0
004DF1CE  mov      eax, dword ptr [rip + 0x1b85b30]  ; -> 02064D04
004DF1D4  mov      dword ptr [rip + 0x1b85afa], eax  ; -> 02064CD4
004DF1DA  mov      eax, dword ptr [rip + 0x1b85b28]  ; -> 02064D08
004DF1E0  mov      dword ptr [rip + 0x1b85af2], eax  ; -> 02064CD8
004DF1E6  mov      dword ptr [rip + 0x1b85ac3], r12d  ; -> 02064CB0
004DF1ED  mov      dword ptr [rip + 0x1b85ac0], r13d  ; -> 02064CB4
004DF1F4  jne      0x4df2a9  ; -> 004DF2A9
004DF1FA  cmp      bx, si
004DF1FD  je       0x4df2a9  ; -> 004DF2A9
004DF203  movups   xmm0, xmmword ptr [rip + 0x1b85a06]  ; -> 02064C10
004DF20A  add      word ptr [rip + 0x1b85ba6], 3  ; -> 02064DB8
004DF212  lea      eax, [r11 + 3]
004DF216  mov      rdx, qword ptr [rsp + 0x128]
004DF21E  add      di, 0x12
004DF222  shl      eax, 4
004DF225  movsxd   rcx, eax
004DF228  lea      eax, [r11 + 9]
004DF22C  shl      eax, 4
004DF22F  mov      word ptr [rip + 0x1b85b7e], di  ; -> 02064DB4
004DF236  movups   xmmword ptr [rcx + r14], xmm0
004DF23B  movsxd   rcx, eax
004DF23E  lea      eax, [r11 + 0xf]
004DF242  movups   xmm0, xmmword ptr [rip + 0x1b859d7]  ; -> 02064C20
004DF249  shl      eax, 4
004DF24C  movups   xmmword ptr [rcx + r14], xmm0
004DF251  movsxd   rcx, eax
004DF254  movups   xmm0, xmmword ptr [rip + 0x1b859d5]  ; -> 02064C30
004DF25B  movups   xmmword ptr [rcx + r14], xmm0
004DF260  mov      rcx, qword ptr [rsp + 0x120]
004DF268  call     0x4c7f00  ; -> 004C7F00 fn
004DF26D  movups   xmm1, xmmword ptr [rip + 0x1b85a1c]  ; -> 02064C90
004DF274  movzx    ebx, word ptr [rip + 0x1b85891]  ; -> 02064B0C
004DF27B  movss    xmm11, dword ptr [rip + 0x1b85970]  ; -> 02064BF4
004DF284  movzx    edi, word ptr [rip + 0x1b85b29]  ; -> 02064DB4
004DF28B  movzx    esi, word ptr [rip + 0x1b85b2a]  ; -> 02064DBC
004DF292  movzx    ebp, word ptr [rip + 0x1b85b27]  ; -> 02064DC0
004DF299  movups   xmm12, xmmword ptr [rip + 0x1b859cf]  ; -> 02064C70
004DF2A1  movups   xmm13, xmmword ptr [rip + 0x1b859d7]  ; -> 02064C80
004DF2A9  addss    xmm11, dword ptr [rip + 0x1b8593e]  ; -> 02064BF0
004DF2B2  inc      si
004DF2B5  movsx    eax, bx
004DF2B8  add      ax, bp
004DF2BB  mov      word ptr [rip + 0x1b85afa], si  ; -> 02064DBC
004DF2C2  mov      word ptr [rip + 0x1b85afb], ax  ; -> 02064DC4
004DF2C9  movzx    eax, word ptr [rip + 0x1b85b04]  ; -> 02064DD4
004DF2D0  movss    dword ptr [rip + 0x1b8591b], xmm11  ; -> 02064BF4
004DF2D9  test     ax, ax
004DF2DC  jle      0x4df305  ; -> 004DF305
004DF2DE  movss    xmm14, dword ptr [rip + 0x1b85905]  ; -> 02064BEC
004DF2E7  movss    xmm2, dword ptr [rip + 0x1b858f1]  ; -> 02064BE0
004DF2EF  movss    xmm4, dword ptr [rip + 0x1b85899]  ; -> 02064B90
004DF2F7  movss    xmm15, dword ptr [rip + 0x1b858dc]  ; -> 02064BDC
004DF300  jmp      0x4de540  ; -> 004DE540
004DF305  mov      r15, qword ptr [rsp + 0x130]
004DF30D  lea      r11, [rsp + 0xe0]
004DF315  movaps   xmm6, xmmword ptr [r11 - 0x10]
004DF31A  movaps   xmm7, xmmword ptr [r11 - 0x20]
004DF31F  movaps   xmm8, xmmword ptr [r11 - 0x30]
004DF324  movaps   xmm9, xmmword ptr [r11 - 0x40]
004DF329  movaps   xmm10, xmmword ptr [r11 - 0x50]
004DF32E  movaps   xmm11, xmmword ptr [r11 - 0x60]
004DF333  movaps   xmm12, xmmword ptr [r11 - 0x70]
004DF338  movaps   xmm13, xmmword ptr [r11 - 0x80]
004DF33D  movaps   xmm14, xmmword ptr [rsp + 0x50]
004DF343  movaps   xmm15, xmmword ptr [rsp + 0x40]
004DF349  mov      rsp, r11
004DF34C  pop      r14
004DF34E  pop      r13
004DF350  pop      r12
004DF352  pop      rdi
004DF353  pop      rsi
004DF354  pop      rbp
004DF355  pop      rbx
004DF356  ret      
```

## 004DF440 (6957 B, extent 004DF440-004E0F6D)

Page context: "820' are two of the 77 rows the [VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md)'s template census decodes; §2.4b there reads the rest of this chain and gives the map — type ''h'' installs '004DF440' and '004E0F70', ''i'' installs '004DCC00' and '004DDDF0', '0xA3' installs '004DB350', '0xA6' and '0xA8' share '004DA8A0', and ''j'' installs '004D7BF0'. **The copied template carries the MPG descriptor verbatim**, which is how the"

```
004DF440  mov      rax, rsp
004DF443  mov      qword ptr [rax + 8], rbx
004DF447  push     rbp
004DF448  push     rsi
004DF449  push     rdi
004DF44A  push     r12
004DF44C  push     r13
004DF44E  push     r14
004DF450  push     r15
004DF452  sub      rsp, 0xc0
004DF459  movsx    r11d, word ptr [rip + 0x1b856ab]  ; -> 02064B0C
004DF461  lea      r13, [rip + 0x1b859c8]  ; -> 02064E30
004DF468  movaps   xmmword ptr [rax - 0x48], xmm6
004DF46C  mov      edx, r11d
004DF46F  movaps   xmmword ptr [rax - 0x58], xmm7
004DF473  movaps   xmmword ptr [rax - 0x68], xmm8
004DF478  movaps   xmmword ptr [rax - 0x78], xmm9
004DF47D  lea      r10d, [r11 + r11]
004DF481  movaps   xmmword ptr [rsp + 0x70], xmm10
004DF487  lea      eax, [r11 + 4]
004DF48B  shl      eax, 4
004DF48E  cdqe     
004DF490  mov      qword ptr [rsp + 0x118], rax
004DF498  movaps   xmmword ptr [rsp + 0x60], xmm11
004DF49E  movaps   xmmword ptr [rsp + 0x50], xmm12
004DF4A4  movzx    r9d, word ptr [rax + r13]
004DF4A9  lea      eax, [r11 + 5]
004DF4AD  movss    xmm12, dword ptr [rip + 0x192337a]  ; -> 01E02830 [u32 0x00000000]
004DF4B6  add      r9w, 2
004DF4BB  shl      eax, 4
004DF4BE  movaps   xmm3, xmm12
004DF4C2  movsxd   rcx, eax
004DF4C5  movaps   xmmword ptr [rsp + 0x40], xmm13
004DF4CB  movaps   xmmword ptr [rsp + 0x30], xmm14
004DF4D1  movaps   xmmword ptr [rsp + 0x20], xmm15
004DF4D7  lea      eax, [r11 + 6]
004DF4DB  shl      edx, 4
004DF4DE  movups   xmm2, xmmword ptr [rcx + r13]
004DF4E3  shl      eax, 4
004DF4E6  movss    xmm13, dword ptr [rip + 0x192334d]  ; -> 01E0283C [f32 1]
004DF4EF  movsxd   rcx, eax
004DF4F2  addss    xmm3, xmm13
004DF4F7  lea      eax, [r11 + 7]
004DF4FB  movaps   xmm1, xmm2
004DF4FE  shl      eax, 4
004DF501  shufps   xmm1, xmm2, 0x55
004DF505  movups   xmm0, xmmword ptr [rcx + r13]
004DF50A  movsxd   rcx, eax
004DF50D  lea      eax, [r11 + 8]
004DF511  shl      eax, 4
004DF514  subss    xmm1, xmm2
004DF518  movups   xmmword ptr [rip + 0x1b856a1], xmm0  ; -> 02064BC0
004DF51F  movups   xmm0, xmmword ptr [rcx + r13]
004DF524  movsxd   rcx, eax
004DF527  lea      eax, [r11 + 9]
004DF52B  shl      eax, 4
004DF52E  movups   xmmword ptr [rip + 0x1b8569b], xmm0  ; -> 02064BD0
004DF535  movups   xmm0, xmmword ptr [rcx + r13]
004DF53A  movsxd   rcx, eax
004DF53D  lea      eax, [r11 + 3]
004DF541  shl      eax, 4
004DF544  movups   xmmword ptr [rip + 0x1b856c5], xmm2  ; -> 02064C10
004DF54B  movups   xmmword ptr [rip + 0x1b8568e], xmm0  ; -> 02064BE0
004DF552  movups   xmm0, xmmword ptr [rcx + r13]
004DF557  movsxd   rcx, eax
004DF55A  lea      eax, [rdx + 0x10]
004DF55D  movss    dword ptr [rip + 0x1b856af], xmm1  ; -> 02064C14
004DF565  movups   xmmword ptr [rip + 0x1b85684], xmm0  ; -> 02064BF0
004DF56C  movups   xmm11, xmmword ptr [rcx + r13]
004DF571  movsxd   rcx, eax
004DF574  movsxd   rax, edx
004DF577  movaps   xmm2, xmm11
004DF57B  subss    xmm3, xmm11
004DF580  mulss    xmm2, dword ptr [rip + 0x413b94]  ; -> 008F311C [f32 3]
004DF588  movaps   xmm10, xmm11
004DF58C  movzx    eax, word ptr [rax + r13]
004DF591  movaps   xmm5, xmm11
004DF595  movups   xmm0, xmmword ptr [rcx + r13]
004DF59A  mov      word ptr [rip + 0x1b8581f], ax  ; -> 02064DC0
004DF5A1  lea      eax, [r11 + 0x13]
004DF5A5  addss    xmm10, dword ptr [rip + 0x192328a]  ; -> 01E02838 [u32 0x00000000]
004DF5AE  shl      eax, 4
004DF5B1  movaps   xmm1, xmm11
004DF5B5  movsxd   rbx, eax
004DF5B8  movaps   xmm7, xmm2
004DF5BB  addss    xmm7, dword ptr [rip + 0x1923271]  ; -> 01E02834 [u32 0x00000000]
004DF5C3  movups   xmmword ptr [rip + 0x1b85635], xmm11  ; -> 02064C00
004DF5CB  movups   xmm8, xmmword ptr [rbx + r13]
004DF5D0  movups   xmmword ptr [rip + 0x1b85559], xmm0  ; -> 02064B30
004DF5D7  mulss    xmm5, xmm13
004DF5DC  mulss    xmm1, xmm11
004DF5E1  lea      eax, [r11 + 0x14]
004DF5E5  mulss    xmm10, xmm2
004DF5EA  shl      eax, 4
004DF5ED  lea      r8, [rip + 0x1b8583c]  ; -> 02064E30
004DF5F4  movsxd   rdi, eax
004DF5F7  addss    xmm12, xmm13
004DF5FC  lea      eax, [r11 + 0x15]
004DF600  movss    dword ptr [rip + 0x1b85653], xmm13  ; -> 02064C5C
004DF609  shl      eax, 4
004DF60C  movaps   xmm6, xmm3
004DF60F  movsxd   rsi, eax
004DF612  xorps    xmm9, xmm9
004DF616  movups   xmm0, xmmword ptr [rdi + r13]
004DF61B  lea      eax, [r11 + 0x16]
004DF61F  mov      dword ptr [rip + 0x1b854db], 0x40400000  ; -> 02064B04
004DF629  mulss    xmm6, xmm3
004DF62D  shl      eax, 4
004DF630  movsxd   rbp, eax
004DF633  lea      eax, [r11 + 0x17]
004DF637  shl      eax, 4
004DF63A  movsxd   r14, eax
004DF63D  lea      eax, [r11 + 0x18]
004DF641  movups   xmmword ptr [rip + 0x1b85668], xmm0  ; -> 02064CB0
004DF648  shl      eax, 4
004DF64B  movups   xmm0, xmmword ptr [rsi + r13]
004DF650  movsxd   r15, eax
004DF653  lea      eax, [r11 + 0x19]
004DF657  movups   xmm15, xmmword ptr [r14 + r13]
004DF65C  shl      eax, 4
004DF65F  movups   xmmword ptr [rip + 0x1b8565a], xmm0  ; -> 02064CC0
004DF666  movsxd   r12, eax
004DF669  lea      eax, [r11 + 0x1a]
004DF66D  movups   xmm0, xmmword ptr [r13 + rbp]
004DF673  shl      eax, 4
004DF676  mulss    xmm7, xmm6
004DF67A  movups   xmmword ptr [rip + 0x1b8564f], xmm0  ; -> 02064CD0
004DF681  movups   xmm0, xmmword ptr [r15 + r13]
004DF686  movss    dword ptr [rsp + 0x110], xmm12
004DF690  movups   xmmword ptr [rip + 0x1b85659], xmm0  ; -> 02064CF0
004DF697  movups   xmm0, xmmword ptr [r12 + r13]
004DF69C  movsxd   r13, eax
004DF69F  mulss    xmm5, xmm1
004DF6A3  movups   xmmword ptr [rip + 0x1b85656], xmm0  ; -> 02064D00
004DF6AA  movups   xmm0, xmmword ptr [r8 + r13]
004DF6AF  mulss    xmm10, xmm3
004DF6B4  movups   xmmword ptr [rip + 0x1b85655], xmm0  ; -> 02064D10
004DF6BB  mulss    xmm6, xmm3
004DF6BF  nop      
004DF6C0  movss    xmm2, dword ptr [rip + 0x1b85508]  ; -> 02064BD0
004DF6C8  movaps   xmm3, xmm5
004DF6CB  mulss    xmm3, dword ptr [rip + 0x1b85501]  ; -> 02064BD4
004DF6D3  movaps   xmm1, xmm10
004DF6D7  mulss    xmm1, dword ptr [rip + 0x1b85515]  ; -> 02064BF4
004DF6DF  movss    xmm0, dword ptr [rip + 0x1b85509]  ; -> 02064BF0
004DF6E7  movss    xmm4, dword ptr [rip + 0x1b854e9]  ; -> 02064BD8
004DF6EF  addss    xmm11, dword ptr [rip + 0x1b8550c]  ; -> 02064C04
004DF6F8  mulss    xmm0, xmm10
004DF6FD  addss    xmm3, xmm1
004DF701  movss    xmm1, dword ptr [rip + 0x1b854d7]  ; -> 02064BE0
004DF709  mulss    xmm1, xmm7
004DF70D  mulss    xmm2, xmm5
004DF711  mulss    xmm4, xmm5
004DF715  movss    xmm5, dword ptr [rip + 0x1b854a7]  ; -> 02064BC4
004DF71D  addss    xmm2, xmm0
004DF721  movss    xmm0, dword ptr [rip + 0x1b854cf]  ; -> 02064BF8
004DF729  mulss    xmm0, xmm10
004DF72E  mulss    xmm5, xmm6
004DF732  addss    xmm2, xmm1
004DF736  movss    dword ptr [rip + 0x1b854c1], xmm11  ; -> 02064C00
004DF73F  movss    xmm1, dword ptr [rip + 0x1b854a1]  ; -> 02064BE8
004DF747  addss    xmm4, xmm0
004DF74B  mulss    xmm1, xmm7
004DF74F  movaps   xmm0, xmm7
004DF752  mulss    xmm0, dword ptr [rip + 0x1b8548a]  ; -> 02064BE4
004DF75A  movss    xmm7, dword ptr [rip + 0x1b85466]  ; -> 02064BC8
004DF762  addss    xmm4, xmm1
004DF766  movss    xmm1, dword ptr [rip + 0x1b8554a]  ; -> 02064CB8
004DF76E  addss    xmm3, xmm0
004DF772  mulss    xmm7, xmm6
004DF776  movss    xmm0, dword ptr [rip + 0x1b85442]  ; -> 02064BC0
004DF77E  mulss    xmm0, xmm6
004DF782  addss    xmm7, xmm4
004DF786  addss    xmm5, xmm3
004DF78A  addss    xmm0, xmm2
004DF78E  movss    dword ptr [rip + 0x1b854c2], xmm7  ; -> 02064C58
004DF796  mulss    xmm1, xmm5
004DF79A  movaps   xmm6, xmm0
004DF79D  movss    dword ptr [rip + 0x1b854af], xmm5  ; -> 02064C54
004DF7A5  movss    xmm0, dword ptr [rip + 0x1b85503]  ; -> 02064CB0
004DF7AD  mulss    xmm0, xmm5
004DF7B1  shufps   xmm6, xmm6, 0
004DF7B5  mulps    xmm6, xmm8
004DF7B9  movss    xmm8, dword ptr [rip + 0x1b8551a]  ; -> 02064CDC
004DF7C2  mulss    xmm8, xmm13
004DF7C7  movups   xmmword ptr [rip + 0x1b85352], xmm6  ; -> 02064B20
004DF7CE  movss    xmm2, dword ptr [rip + 0x1b8534e]  ; -> 02064B24
004DF7D6  addss    xmm6, xmm0
004DF7DA  movss    xmm0, dword ptr [rip + 0x1b854d2]  ; -> 02064CB4
004DF7E2  movss    xmm4, dword ptr [rip + 0x1b85342]  ; -> 02064B2C
004DF7EA  movss    xmm3, dword ptr [rip + 0x1b85336]  ; -> 02064B28
004DF7F2  mulss    xmm0, xmm5
004DF7F6  addss    xmm3, xmm1
004DF7FA  movaps   xmm1, xmm7
004DF7FD  mulss    xmm1, dword ptr [rip + 0x1b854bf]  ; -> 02064CC4
004DF805  addss    xmm2, xmm0
004DF809  movss    xmm0, dword ptr [rip + 0x1b854ab]  ; -> 02064CBC
004DF811  mulss    xmm0, xmm5
004DF815  addss    xmm4, xmm0
004DF819  movaps   xmm0, xmm7
004DF81C  mulss    xmm0, dword ptr [rip + 0x1b8549c]  ; -> 02064CC0
004DF824  addss    xmm2, xmm1
004DF828  addss    xmm6, xmm0
004DF82C  movaps   xmm0, xmm7
004DF82F  mulss    xmm0, dword ptr [rip + 0x1b85491]  ; -> 02064CC8
004DF837  mulss    xmm7, dword ptr [rip + 0x1b8548d]  ; -> 02064CCC
004DF83F  addss    xmm3, xmm0
004DF843  movss    xmm0, dword ptr [rip + 0x1b85485]  ; -> 02064CD0
004DF84B  mulss    xmm0, xmm13
004DF850  addss    xmm4, xmm7
004DF854  movss    xmm7, dword ptr [rip + 0x1b8547c]  ; -> 02064CD8
004DF85C  mulss    xmm7, xmm13
004DF861  addss    xmm0, xmm6
004DF865  movss    xmm6, dword ptr [rip + 0x1b85467]  ; -> 02064CD4
004DF86D  mulss    xmm6, xmm13
004DF872  addss    xmm7, xmm3
004DF876  addss    xmm6, xmm2
004DF87A  movss    dword ptr [rip + 0x1b853fe], xmm0  ; -> 02064C80
004DF882  movss    dword ptr [rip + 0x1b853fe], xmm7  ; -> 02064C88
004DF88A  movss    dword ptr [rip + 0x1b853f2], xmm6  ; -> 02064C84
004DF892  movaps   xmm5, xmm0
004DF895  addss    xmm8, xmm4
004DF89A  shufps   xmm5, xmm5, 0
004DF89E  movaps   xmm0, xmm6
004DF8A1  mulss    xmm0, dword ptr [rip + 0x1b85447]  ; -> 02064CF0
004DF8A9  movaps   xmm1, xmm6
004DF8AC  mulss    xmm1, dword ptr [rip + 0x1b85444]  ; -> 02064CF8
004DF8B4  movaps   xmm14, xmm11
004DF8B8  mulss    xmm14, dword ptr [rip + 0x41385b]  ; -> 008F311C [f32 3]
004DF8C1  movaps   xmm10, xmm11
004DF8C5  addss    xmm10, dword ptr [rip + 0x1922f6a]  ; -> 01E02838 [u32 0x00000000]
004DF8CE  mulps    xmm5, xmm15
004DF8D2  movss    dword ptr [rip + 0x1b853b1], xmm8  ; -> 02064C8C
004DF8DB  movss    dword ptr [rip + 0x1b8535c], xmm14  ; -> 02064C40
004DF8E4  movups   xmmword ptr [rip + 0x1b85235], xmm5  ; -> 02064B20
004DF8EB  movss    xmm2, dword ptr [rip + 0x1b85231]  ; -> 02064B24
004DF8F3  addss    xmm5, xmm0
004DF8F7  movss    xmm3, dword ptr [rip + 0x1b85229]  ; -> 02064B28
004DF8FF  movaps   xmm0, xmm6
004DF902  mulss    xmm0, dword ptr [rip + 0x1b853ea]  ; -> 02064CF4
004DF90A  addss    xmm3, xmm1
004DF90E  movss    xmm4, dword ptr [rip + 0x1b85216]  ; -> 02064B2C
004DF916  movaps   xmm1, xmm7
004DF919  mulss    xmm1, dword ptr [rip + 0x1b853e3]  ; -> 02064D04
004DF921  mulss    xmm6, dword ptr [rip + 0x1b853d3]  ; -> 02064CFC
004DF929  addss    xmm2, xmm0
004DF92D  movaps   xmm0, xmm7
004DF930  mulss    xmm0, dword ptr [rip + 0x1b853c8]  ; -> 02064D00
004DF938  addss    xmm2, xmm1
004DF93C  movaps   xmm1, xmm8
004DF940  mulss    xmm1, dword ptr [rip + 0x1b853cc]  ; -> 02064D14
004DF948  addss    xmm4, xmm6
004DF94C  addss    xmm5, xmm0
004DF950  movaps   xmm0, xmm7
004DF953  mulss    xmm0, dword ptr [rip + 0x1b853ad]  ; -> 02064D08
004DF95B  mulss    xmm7, dword ptr [rip + 0x1b853a9]  ; -> 02064D0C
004DF963  addss    xmm1, xmm2
004DF967  addss    xmm3, xmm0
004DF96B  movss    dword ptr [rip + 0x1b851ad], xmm5  ; -> 02064B20
004DF973  movaps   xmm0, xmm8
004DF977  movss    dword ptr [rip + 0x1b851a5], xmm2  ; -> 02064B24
004DF97F  mulss    xmm0, dword ptr [rip + 0x1b85389]  ; -> 02064D10
004DF987  addss    xmm4, xmm7
004DF98B  movss    dword ptr [rip + 0x1b852d1], xmm1  ; -> 02064C64
004DF993  movss    dword ptr [rip + 0x1b8518d], xmm3  ; -> 02064B28
004DF99B  addss    xmm0, xmm5
004DF99F  movss    dword ptr [rip + 0x1b85185], xmm4  ; -> 02064B2C
004DF9A7  movss    dword ptr [rip + 0x1b852b1], xmm0  ; -> 02064C60
004DF9AF  movaps   xmm0, xmm8
004DF9B3  mulss    xmm8, dword ptr [rip + 0x1b85360]  ; -> 02064D1C
004DF9BC  mulss    xmm0, dword ptr [rip + 0x1b85354]  ; -> 02064D18
004DF9C4  addss    xmm8, xmm4
004DF9C9  addss    xmm0, xmm3
004DF9CD  ucomiss  xmm8, xmm9
004DF9D1  movss    dword ptr [rip + 0x1b8528f], xmm0  ; -> 02064C68
004DF9D9  movss    dword ptr [rip + 0x1b8528a], xmm8  ; -> 02064C6C
004DF9E2  jp       0x4df9f0  ; -> 004DF9F0
004DF9E4  jne      0x4df9f0  ; -> 004DF9F0
004DF9E6  movss    xmm2, dword ptr [rip + 0x420972]  ; -> 00900360 [u32 0x7F7FFFFF]
004DF9EE  jmp      0x4df9f9  ; -> 004DF9F9
004DF9F0  movaps   xmm2, xmm13
004DF9F4  divss    xmm2, xmm8
004DF9F9  movups   xmm0, xmmword ptr [rdi + r8]
004DF9FE  movsx    edx, r10w
004DFA02  dec      r9w
004DFA06  movups   xmm8, xmmword ptr [rbx + r8]
004DFA0B  inc      r10w
004DFA0F  movups   xmm15, xmmword ptr [r14 + r8]
004DFA14  lea      eax, [rdx + 0x2bc]
004DFA1A  movups   xmmword ptr [rip + 0x1b8528f], xmm0  ; -> 02064CB0
004DFA21  shl      eax, 4
004DFA24  movups   xmm0, xmmword ptr [rsi + r8]
004DFA29  movsxd   rcx, eax
004DFA2C  lea      eax, [rdx + 0x80]
004DFA32  subss    xmm12, xmm11
004DFA37  movss    dword ptr [rip + 0x1b850c1], xmm2  ; -> 02064B00
004DFA3F  movups   xmmword ptr [rip + 0x1b8527a], xmm0  ; -> 02064CC0
004DFA46  shl      eax, 4
004DFA49  mulss    xmm10, xmm14
004DFA4E  movaps   xmm1, xmm11
004DFA52  mulss    xmm1, xmm11
004DFA57  movaps   xmm6, xmm12
004DFA5B  mulss    xmm6, xmm12
004DFA60  movaps   xmm5, xmm11
004DFA64  mulss    xmm5, xmm13
004DFA69  movaps   xmm7, xmm14
004DFA6D  movss    dword ptr [rip + 0x1b851db], xmm1  ; -> 02064C50
004DFA75  movss    dword ptr [rip + 0x1b851b2], xmm12  ; -> 02064C30
004DFA7E  mulss    xmm5, xmm1
004DFA82  movaps   xmm1, xmm2
004DFA85  shufps   xmm1, xmm1, 0
004DFA89  mulss    xmm10, xmm12
004DFA8E  movups   xmm0, xmmword ptr [r8 + rbp]
004DFA93  movups   xmm2, xmmword ptr [rip + 0x1b851c6]  ; -> 02064C60
004DFA9A  addss    xmm7, dword ptr [rip + 0x1922d92]  ; -> 01E02834 [u32 0x00000000]
004DFAA2  mulps    xmm2, xmm1
004DFAA5  movups   xmmword ptr [rip + 0x1b85224], xmm0  ; -> 02064CD0
004DFAAC  mulss    xmm7, xmm6
004DFAB0  mulss    xmm6, xmm12
004DFAB5  movss    xmm12, dword ptr [rsp + 0x110]
004DFABF  movups   xmm0, xmmword ptr [r15 + r8]
004DFAC4  movups   xmmword ptr [rip + 0x1b85195], xmm2  ; -> 02064C60
004DFACB  movups   xmmword ptr [rip + 0x1b8521e], xmm0  ; -> 02064CF0
004DFAD2  movups   xmm0, xmmword ptr [r12 + r8]
004DFAD7  movups   xmmword ptr [rip + 0x1b85222], xmm0  ; -> 02064D00
004DFADE  movups   xmm0, xmmword ptr [r8 + r13]
004DFAE3  movups   xmmword ptr [rip + 0x1b85226], xmm0  ; -> 02064D10
004DFAEA  movups   xmm0, xmmword ptr [rip + 0x1b8518f]  ; -> 02064C80
004DFAF1  movups   xmmword ptr [rcx + r8], xmm0
004DFAF6  movsxd   rcx, eax
004DFAF9  movups   xmmword ptr [rcx + r8], xmm2
004DFAFE  cmp      r9w, r11w
004DFB02  jne      0x4df6c0  ; -> 004DF6C0
004DFB08  mov      rax, qword ptr [rsp + 0x118]
004DFB10  lea      r15, [rip + 0x1b85319]  ; -> 02064E30
004DFB17  movsx    r8d, r11w
004DFB1B  add      r8w, r11w
004DFB1F  movss    dword ptr [rip + 0x1b850f9], xmm6  ; -> 02064C20
004DFB27  movsx    edx, r8w
004DFB2B  movzx    eax, word ptr [rax + r15]
004DFB30  mov      word ptr [rip + 0x1b8529d], ax  ; -> 02064DD4
004DFB37  movss    dword ptr [rip + 0x1b850e8], xmm10  ; -> 02064C28
004DFB40  lea      eax, [rdx + 0x80]
004DFB46  movss    dword ptr [rip + 0x1b850de], xmm5  ; -> 02064C2C
004DFB4E  shl      eax, 4
004DFB51  movsxd   rcx, eax
004DFB54  lea      eax, [rdx + 0x81]
004DFB5A  shl      eax, 4
004DFB5D  movss    dword ptr [rip + 0x1b850bf], xmm7  ; -> 02064C24
004DFB65  movups   xmmword ptr [rip + 0x1b85133], xmm8  ; -> 02064CA0
004DFB6D  mov      word ptr [rip + 0x1b85263], r8w  ; -> 02064DD8
004DFB75  movups   xmm1, xmmword ptr [rcx + r15]
004DFB7A  movsxd   rcx, eax
004DFB7D  movups   xmmword ptr [rip + 0x1b8515b], xmm15  ; -> 02064CE0
004DFB85  movups   xmmword ptr [rip + 0x1b850d4], xmm1  ; -> 02064C60
004DFB8C  movups   xmm0, xmmword ptr [rcx + r15]
004DFB91  movups   xmm2, xmm0
004DFB94  movups   xmmword ptr [rip + 0x1b850d5], xmm0  ; -> 02064C70
004DFB9B  movss    dword ptr [rip + 0x1b850cd], xmm2  ; -> 02064C70
004DFBA3  subss    xmm0, xmm1
004DFBA7  shufps   xmm2, xmm2, 0x55
004DFBAB  movss    dword ptr [rip + 0x1b850c1], xmm2  ; -> 02064C74
004DFBB3  subss    xmm2, dword ptr [rip + 0x1b850a9]  ; -> 02064C64
004DFBBB  ucomiss  xmm0, xmm9
004DFBBF  movss    dword ptr [rip + 0x1b8509d], xmm2  ; -> 02064C64
004DFBC7  movss    dword ptr [rip + 0x1b85091], xmm0  ; -> 02064C60
004DFBCF  jp       0x4dfbd3  ; -> 004DFBD3
004DFBD1  je       0x4dfbdb  ; -> 004DFBDB
004DFBD3  ucomiss  xmm2, xmm9
004DFBD7  jp       0x4dfbf0  ; -> 004DFBF0
004DFBD9  jne      0x4dfbf0  ; -> 004DFBF0
004DFBDB  call     0x22cc40  ; -> 0022CC40 fn
004DFBE0  movss    xmm2, dword ptr [rip + 0x1b8507c]  ; -> 02064C64
004DFBE8  movss    xmm0, dword ptr [rip + 0x1b85070]  ; -> 02064C60
004DFBF0  comiss   xmm9, xmm0
004DFBF4  ja       0x4dfbfc  ; -> 004DFBFC
004DFBF6  comiss   xmm9, xmm2
004DFBFA  jbe      0x4dfc01  ; -> 004DFC01
004DFBFC  call     0x22cc30  ; -> 0022CC30 fn
004DFC01  call     0x22cc20  ; -> 0022CC20 fn
004DFC06  movss    xmm1, dword ptr [rip + 0x1922c22]  ; -> 01E02830 [u32 0x00000000]
004DFC0E  subss    xmm1, dword ptr [rip + 0x1b8504e]  ; -> 02064C64
004DFC16  movss    xmm0, dword ptr [rip + 0x1922c16]  ; -> 01E02834 [u32 0x00000000]
004DFC1E  subss    xmm0, dword ptr [rip + 0x1b8503a]  ; -> 02064C60
004DFC26  movss    xmm6, dword ptr [rip + 0x1922c0e]  ; -> 01E0283C [f32 1]
004DFC2E  movsd    xmm10, qword ptr [rip + 0x180c149]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004DFC37  movss    dword ptr [rip + 0x1b85061], xmm1  ; -> 02064CA0
004DFC3F  mulss    xmm1, xmm1
004DFC43  movss    dword ptr [rip + 0x1b85059], xmm0  ; -> 02064CA4
004DFC4B  mulss    xmm0, xmm0
004DFC4F  movss    dword ptr [rip + 0x1b85029], xmm1  ; -> 02064C80
004DFC57  mulss    xmm1, xmm6
004DFC5B  movss    dword ptr [rip + 0x1b85021], xmm0  ; -> 02064C84
004DFC63  mulss    xmm0, xmm6
004DFC67  movss    dword ptr [rip + 0x1b84ebd], xmm1  ; -> 02064B2C
004DFC6F  addss    xmm0, xmm1
004DFC73  movss    dword ptr [rip + 0x1b85011], xmm0  ; -> 02064C8C
004DFC7B  cvtps2pd xmm0, xmm0
004DFC7E  andps    xmm0, xmm10
004DFC82  cvtpd2ps xmm0, xmm0
004DFC86  call     0x861f14  ; -> 00861F14 fn
004DFC8B  ucomiss  xmm0, xmm9
004DFC8F  jp       0x4dfc9f  ; -> 004DFC9F
004DFC91  jne      0x4dfc9f  ; -> 004DFC9F
004DFC93  mov      dword ptr [rip + 0x1b84e63], 0x7f7fffff  ; -> 02064B00
004DFC9D  jmp      0x4dfcab  ; -> 004DFCAB
004DFC9F  divss    xmm6, xmm0
004DFCA3  movss    dword ptr [rip + 0x1b84e55], xmm6  ; -> 02064B00
004DFCAB  movsx    edx, word ptr [rip + 0x1b85126]  ; -> 02064DD8
004DFCB2  lea      eax, [rdx + 0x81]
004DFCB8  shl      eax, 4
004DFCBB  movsxd   rcx, eax
004DFCBE  lea      eax, [rdx + 0x82]
004DFCC4  shl      eax, 4
004DFCC7  movups   xmm1, xmmword ptr [rcx + r15]
004DFCCC  movsxd   rcx, eax
004DFCCF  movups   xmmword ptr [rip + 0x1b84f8a], xmm1  ; -> 02064C60
004DFCD6  movups   xmm0, xmmword ptr [rcx + r15]
004DFCDB  movups   xmm2, xmm0
004DFCDE  movups   xmmword ptr [rip + 0x1b84f8b], xmm0  ; -> 02064C70
004DFCE5  movss    dword ptr [rip + 0x1b84f83], xmm2  ; -> 02064C70
004DFCED  subss    xmm0, xmm1
004DFCF1  shufps   xmm2, xmm2, 0x55
004DFCF5  movss    dword ptr [rip + 0x1b84f77], xmm2  ; -> 02064C74
004DFCFD  subss    xmm2, dword ptr [rip + 0x1b84f5f]  ; -> 02064C64
004DFD05  ucomiss  xmm0, xmm9
004DFD09  movss    dword ptr [rip + 0x1b84f53], xmm2  ; -> 02064C64
004DFD11  movss    dword ptr [rip + 0x1b84f47], xmm0  ; -> 02064C60
004DFD19  jp       0x4dfd1d  ; -> 004DFD1D
004DFD1B  je       0x4dfd25  ; -> 004DFD25
004DFD1D  ucomiss  xmm2, xmm9
004DFD21  jp       0x4dfd3a  ; -> 004DFD3A
004DFD23  jne      0x4dfd3a  ; -> 004DFD3A
004DFD25  call     0x22cc40  ; -> 0022CC40 fn
004DFD2A  movss    xmm2, dword ptr [rip + 0x1b84f32]  ; -> 02064C64
004DFD32  movss    xmm0, dword ptr [rip + 0x1b84f26]  ; -> 02064C60
004DFD3A  comiss   xmm9, xmm0
004DFD3E  ja       0x4dfd46  ; -> 004DFD46
004DFD40  comiss   xmm9, xmm2
004DFD44  jbe      0x4dfd4b  ; -> 004DFD4B
004DFD46  call     0x22cc30  ; -> 0022CC30 fn
004DFD4B  call     0x22cc20  ; -> 0022CC20 fn
004DFD50  movsx    ebx, word ptr [rip + 0x1b85081]  ; -> 02064DD8
004DFD57  movss    xmm1, dword ptr [rip + 0x1b84f45]  ; -> 02064CA4
004DFD5F  movss    xmm4, dword ptr [rip + 0x1922ac9]  ; -> 01E02830 [u32 0x00000000]
004DFD67  subss    xmm4, dword ptr [rip + 0x1b84ef5]  ; -> 02064C64
004DFD6F  movss    xmm3, dword ptr [rip + 0x1922abd]  ; -> 01E02834 [u32 0x00000000]
004DFD77  lea      eax, [rbx + 0x352]
004DFD7D  subss    xmm3, dword ptr [rip + 0x1b84edb]  ; -> 02064C60
004DFD85  movss    xmm8, dword ptr [rip + 0x1922aae]  ; -> 01E0283C [f32 1]
004DFD8E  inc      bx
004DFD91  mulss    xmm1, dword ptr [rip + 0x1b84d67]  ; -> 02064B00
004DFD99  movzx    r8d, word ptr [rip + 0x1b84d6b]  ; -> 02064B0C
004DFDA1  movaps   xmm0, xmm4
004DFDA4  shl      eax, 4
004DFDA7  cmp      r8w, word ptr [rip + 0x1b85025]  ; -> 02064DD4
004DFDAF  movaps   xmm6, xmm3
004DFDB2  mulss    xmm0, xmm4
004DFDB6  movsxd   rcx, eax
004DFDB9  mulss    xmm6, xmm3
004DFDBD  mov      word ptr [rip + 0x1b85014], bx  ; -> 02064DD8
004DFDC4  movss    dword ptr [rip + 0x1b84eb4], xmm0  ; -> 02064C80
004DFDCC  mulss    xmm0, xmm8
004DFDD1  movss    dword ptr [rip + 0x1b84eab], xmm6  ; -> 02064C84
004DFDD9  movss    dword ptr [rip + 0x1b84ec3], xmm1  ; -> 02064CA4
004DFDE1  movss    xmm1, dword ptr [rip + 0x1b84ed3]  ; -> 02064CBC
004DFDE9  movss    dword ptr [rip + 0x1b84d3b], xmm0  ; -> 02064B2C
004DFDF1  mulss    xmm6, xmm8
004DFDF6  movss    dword ptr [rip + 0x1b84eb2], xmm4  ; -> 02064CB0
004DFDFE  movss    dword ptr [rip + 0x1b84eae], xmm3  ; -> 02064CB4
004DFE06  addss    xmm6, xmm0
004DFE0A  movss    dword ptr [rip + 0x1b84e7e], xmm4  ; -> 02064C90
004DFE12  movss    xmm0, dword ptr [rip + 0x1b84e86]  ; -> 02064CA0
004DFE1A  mulss    xmm0, dword ptr [rip + 0x1b84cde]  ; -> 02064B00
004DFE22  movss    dword ptr [rip + 0x1b84e6a], xmm3  ; -> 02064C94
004DFE2A  movss    dword ptr [rip + 0x1b84e5a], xmm6  ; -> 02064C8C
004DFE32  movss    dword ptr [rip + 0x1b84e66], xmm0  ; -> 02064CA0
004DFE3A  movups   xmm2, xmmword ptr [rip + 0x1b84e5f]  ; -> 02064CA0
004DFE41  movss    xmm0, dword ptr [rip + 0x1b84e6f]  ; -> 02064CB8
004DFE49  movups   xmmword ptr [rcx + r15], xmm2
004DFE4E  movss    dword ptr [rip + 0x1b84e42], xmm0  ; -> 02064C98
004DFE56  movss    dword ptr [rip + 0x1b84e3e], xmm1  ; -> 02064C9C
004DFE5E  je       0x4e00c3  ; -> 004E00C3
004DFE64  movss    xmm7, dword ptr [rip + 0x180bd04]  ; -> 01CEBB70 [f32 0.5]
004DFE6C  nop      dword ptr [rax]
004DFE70  cvtps2pd xmm0, xmm6
004DFE73  andps    xmm0, xmm10
004DFE77  cvtpd2ps xmm0, xmm0
004DFE7B  call     0x861f14  ; -> 00861F14 fn
004DFE80  ucomiss  xmm0, xmm9
004DFE84  jp       0x4dfe94  ; -> 004DFE94
004DFE86  jne      0x4dfe94  ; -> 004DFE94
004DFE88  mov      dword ptr [rip + 0x1b84c6e], 0x7f7fffff  ; -> 02064B00
004DFE92  jmp      0x4dfea2  ; -> 004DFEA2
004DFE94  divss    xmm8, xmm0
004DFE99  movss    dword ptr [rip + 0x1b84c5e], xmm8  ; -> 02064B00
004DFEA2  movsx    edx, bx
004DFEA5  lea      eax, [rdx + 0x81]
004DFEAB  shl      eax, 4
004DFEAE  movsxd   rcx, eax
004DFEB1  lea      eax, [rdx + 0x82]
004DFEB7  shl      eax, 4
004DFEBA  movups   xmm1, xmmword ptr [rcx + r15]
004DFEBF  movsxd   rcx, eax
004DFEC2  movups   xmmword ptr [rip + 0x1b84d97], xmm1  ; -> 02064C60
004DFEC9  movups   xmm0, xmmword ptr [rcx + r15]
004DFECE  movups   xmm2, xmm0
004DFED1  movups   xmmword ptr [rip + 0x1b84d98], xmm0  ; -> 02064C70
004DFED8  movss    dword ptr [rip + 0x1b84d90], xmm2  ; -> 02064C70
004DFEE0  subss    xmm0, xmm1
004DFEE4  shufps   xmm2, xmm2, 0x55
004DFEE8  movss    dword ptr [rip + 0x1b84d84], xmm2  ; -> 02064C74
004DFEF0  subss    xmm2, dword ptr [rip + 0x1b84d6c]  ; -> 02064C64
004DFEF8  ucomiss  xmm0, xmm9
004DFEFC  movss    dword ptr [rip + 0x1b84d60], xmm2  ; -> 02064C64
004DFF04  movss    dword ptr [rip + 0x1b84d54], xmm0  ; -> 02064C60
004DFF0C  jp       0x4dff10  ; -> 004DFF10
004DFF0E  je       0x4dff18  ; -> 004DFF18
004DFF10  ucomiss  xmm2, xmm9
004DFF14  jp       0x4dff2d  ; -> 004DFF2D
004DFF16  jne      0x4dff2d  ; -> 004DFF2D
004DFF18  call     0x22cc40  ; -> 0022CC40 fn
004DFF1D  movss    xmm2, dword ptr [rip + 0x1b84d3f]  ; -> 02064C64
004DFF25  movss    xmm0, dword ptr [rip + 0x1b84d33]  ; -> 02064C60
004DFF2D  comiss   xmm9, xmm0
004DFF31  ja       0x4dff39  ; -> 004DFF39
004DFF33  comiss   xmm9, xmm2
004DFF37  jbe      0x4dff3e  ; -> 004DFF3E
004DFF39  call     0x22cc30  ; -> 0022CC30 fn
004DFF3E  call     0x22cc20  ; -> 0022CC20 fn
004DFF43  movss    xmm2, dword ptr [rip + 0x1b84d49]  ; -> 02064C94
004DFF4B  movss    xmm3, dword ptr [rip + 0x1b84d3d]  ; -> 02064C90
004DFF53  movsx    ebx, word ptr [rip + 0x1b84e7e]  ; -> 02064DD8
004DFF5A  movss    xmm5, dword ptr [rip + 0x19228ce]  ; -> 01E02830 [u32 0x00000000]
004DFF62  subss    xmm5, dword ptr [rip + 0x1b84cfa]  ; -> 02064C64
004DFF6A  movss    xmm4, dword ptr [rip + 0x19228c2]  ; -> 01E02834 [u32 0x00000000]
004DFF72  subss    xmm4, dword ptr [rip + 0x1b84ce6]  ; -> 02064C60
004DFF7A  mulss    xmm2, dword ptr [rip + 0x1b84b7e]  ; -> 02064B00
004DFF82  lea      eax, [rbx + 0x352]
004DFF88  inc      bx
004DFF8B  movzx    edx, word ptr [rip + 0x1b84e42]  ; -> 02064DD4
004DFF92  movss    xmm8, dword ptr [rip + 0x19228a1]  ; -> 01E0283C [f32 1]
004DFF9B  movaps   xmm1, xmm5
004DFF9E  mulss    xmm3, dword ptr [rip + 0x1b84b5a]  ; -> 02064B00
004DFFA6  dec      dx
004DFFA9  movzx    r8d, word ptr [rip + 0x1b84b5b]  ; -> 02064B0C
004DFFB1  mulss    xmm1, xmm5
004DFFB5  movaps   xmm0, xmm2
004DFFB8  shl      eax, 4
004DFFBB  movsxd   rcx, eax
004DFFBE  movaps   xmm6, xmm4
004DFFC1  mulss    xmm6, xmm4
004DFFC5  mov      word ptr [rip + 0x1b84e08], dx  ; -> 02064DD4
004DFFCC  movss    dword ptr [rip + 0x1b84cac], xmm1  ; -> 02064C80
004DFFD4  mulss    xmm1, xmm8
004DFFD9  mov      dword ptr [rip + 0x1b84b21], 0x3f000000  ; -> 02064B04
004DFFE3  movss    dword ptr [rip + 0x1b84c99], xmm6  ; -> 02064C84
004DFFEB  mulss    xmm6, xmm8
004DFFF0  mov      word ptr [rip + 0x1b84de1], bx  ; -> 02064DD8
004DFFF7  movss    dword ptr [rip + 0x1b84b2d], xmm1  ; -> 02064B2C
004DFFFF  movss    dword ptr [rip + 0x1b84ca9], xmm5  ; -> 02064CB0
004E0007  movss    dword ptr [rip + 0x1b84ca5], xmm4  ; -> 02064CB4
004E000F  addss    xmm6, xmm1
004E0013  movss    dword ptr [rip + 0x1b84c75], xmm5  ; -> 02064C90
004E001B  movaps   xmm1, xmm3
004E001E  movss    dword ptr [rip + 0x1b84c6e], xmm4  ; -> 02064C94
004E0026  addss    xmm0, dword ptr [rip + 0x1b84c76]  ; -> 02064CA4
004E002E  movss    dword ptr [rip + 0x1b84c6e], xmm2  ; -> 02064CA4
004E0036  movss    dword ptr [rip + 0x1b84c4e], xmm6  ; -> 02064C8C
004E003E  addss    xmm1, dword ptr [rip + 0x1b84c5a]  ; -> 02064CA0
004E0046  movss    dword ptr [rip + 0x1b84c52], xmm3  ; -> 02064CA0
004E004E  mulss    xmm0, xmm7
004E0052  mulss    xmm1, xmm7
004E0056  movss    dword ptr [rip + 0x1b84c16], xmm0  ; -> 02064C74
004E005E  movss    xmm0, dword ptr [rip + 0x1b84c32]  ; -> 02064C98
004E0066  movss    dword ptr [rip + 0x1b84c02], xmm1  ; -> 02064C70
004E006E  movss    xmm1, dword ptr [rip + 0x1b84c26]  ; -> 02064C9C
004E0076  movss    dword ptr [rip + 0x1b84c2a], xmm0  ; -> 02064CA8
004E007E  movss    dword ptr [rip + 0x1b84c26], xmm1  ; -> 02064CAC
004E0086  movss    xmm1, dword ptr [rip + 0x1b84c2e]  ; -> 02064CBC
004E008E  movss    dword ptr [rip + 0x1b84c06], xmm1  ; -> 02064C9C
004E0096  movups   xmm0, xmmword ptr [rip + 0x1b84bd3]  ; -> 02064C70
004E009D  movups   xmmword ptr [rcx + r15], xmm0
004E00A2  movss    xmm0, dword ptr [rip + 0x1b84c0e]  ; -> 02064CB8
004E00AA  movss    dword ptr [rip + 0x1b84be6], xmm0  ; -> 02064C98
004E00B2  cmp      r8w, dx
004E00B6  jne      0x4dfe70  ; -> 004DFE70
004E00BC  movups   xmm2, xmmword ptr [rip + 0x1b84bdd]  ; -> 02064CA0
004E00C3  movss    xmm12, dword ptr [rip + 0x180bbb8]  ; -> 01CEBC84 [f32 16]
004E00CC  mov      ebp, 0xe0
004E00D1  movss    xmm1, dword ptr [rip + 0x1b84b2f]  ; -> 02064C08
004E00D9  movsx    r9d, r8w
004E00DD  movsx    eax, bx
004E00E0  add      eax, 0x352
004E00E5  shl      eax, 4
004E00E8  movsxd   rcx, eax
004E00EB  lea      eax, [r9 + 4]
004E00EF  shl      eax, 4
004E00F2  movups   xmmword ptr [rcx + r15], xmm2
004E00F7  movsxd   rcx, eax
004E00FA  movzx    eax, word ptr [rcx + r15]
004E00FF  add      ax, 2
004E0103  add      r9w, r8w
004E0107  mov      word ptr [rip + 0x1b84cc6], ax  ; -> 02064DD4
004E010E  mov      word ptr [rip + 0x1b84cc2], r9w  ; -> 02064DD8
004E0116  nop      word ptr [rax + rax]
004E0120  mulss    xmm1, dword ptr [rip + 0x1b84aec]  ; -> 02064C14
004E0128  movsx    ecx, r9w
004E012C  movups   xmm0, xmmword ptr [rip + 0x1b84bad]  ; -> 02064CE0
004E0133  addss    xmm1, dword ptr [rip + 0x1b84ad5]  ; -> 02064C10
004E013B  lea      eax, [rcx + 0x2bc]
004E0141  shl      eax, 4
004E0144  movsxd   rdx, eax
004E0147  lea      eax, [rcx + 0x352]
004E014D  shl      eax, 4
004E0150  movsxd   rcx, eax
004E0153  movups   xmm7, xmmword ptr [rdx + r15]
004E0158  movups   xmm10, xmmword ptr [rcx + r15]
004E015D  movups   xmmword ptr [rip + 0x1b84afc], xmm7  ; -> 02064C60
004E0164  movaps   xmm6, xmm7
004E0167  movaps   xmm2, xmm7
004E016A  shufps   xmm2, xmm7, 0x55
004E016E  movups   xmmword ptr [rip + 0x1b84afa], xmm10  ; -> 02064C70
004E0176  movss    xmm11, dword ptr [rip + 0x1b84af5]  ; -> 02064C74
004E017F  mulss    xmm10, xmm1
004E0184  mulss    xmm11, xmm1
004E0189  movaps   xmm1, xmm2
004E018C  mulss    xmm1, dword ptr [rip + 0x1b84b64]  ; -> 02064CF8
004E0194  shufps   xmm6, xmm6, 0
004E0198  mulps    xmm6, xmm0
004E019B  movaps   xmm0, xmm2
004E019E  mulss    xmm0, dword ptr [rip + 0x1b84b4a]  ; -> 02064CF0
004E01A6  movups   xmmword ptr [rip + 0x1b84af3], xmm7  ; -> 02064CA0
004E01AD  movups   xmmword ptr [rip + 0x1b8496c], xmm6  ; -> 02064B20
004E01B4  movss    xmm5, dword ptr [rip + 0x1b84970]  ; -> 02064B2C
004E01BC  addss    xmm6, xmm0
004E01C0  movss    xmm3, dword ptr [rip + 0x1b8495c]  ; -> 02064B24
004E01C8  movaps   xmm0, xmm2
004E01CB  mulss    xmm0, dword ptr [rip + 0x1b84b21]  ; -> 02064CF4
004E01D3  mulss    xmm2, dword ptr [rip + 0x1b84b21]  ; -> 02064CFC
004E01DB  movss    xmm4, dword ptr [rip + 0x1b84945]  ; -> 02064B28
004E01E3  addss    xmm3, xmm0
004E01E7  addss    xmm4, xmm1
004E01EB  movss    dword ptr [rip + 0x1b84a7c], xmm10  ; -> 02064C70
004E01F4  addss    xmm5, xmm2
004E01F8  movss    dword ptr [rip + 0x1b84a73], xmm11  ; -> 02064C74
004E0201  movaps   xmm2, xmm7
004E0204  shufps   xmm2, xmm7, 0xaa
004E0208  shufps   xmm7, xmm7, 0xff
004E020C  movaps   xmm0, xmm2
004E020F  mulss    xmm0, dword ptr [rip + 0x1b84ae9]  ; -> 02064D00
004E0217  movaps   xmm1, xmm2
004E021A  mulss    xmm1, dword ptr [rip + 0x1b84ae2]  ; -> 02064D04
004E0222  addss    xmm6, xmm0
004E0226  movaps   xmm0, xmm2
004E0229  mulss    xmm0, dword ptr [rip + 0x1b84ad7]  ; -> 02064D08
004E0231  mulss    xmm2, dword ptr [rip + 0x1b84ad3]  ; -> 02064D0C
004E0239  addss    xmm3, xmm1
004E023D  addss    xmm4, xmm0
004E0241  movss    dword ptr [rip + 0x1b848d7], xmm6  ; -> 02064B20
004E0249  movaps   xmm0, xmm7
004E024C  movaps   xmm1, xmm7
004E024F  mulss    xmm0, dword ptr [rip + 0x1b84ab9]  ; -> 02064D10
004E0257  addss    xmm5, xmm2
004E025B  mulss    xmm1, dword ptr [rip + 0x1b84ab1]  ; -> 02064D14
004E0263  addss    xmm0, xmm6
004E0267  movss    dword ptr [rip + 0x1b848b5], xmm3  ; -> 02064B24
004E026F  movss    dword ptr [rip + 0x1b848b1], xmm4  ; -> 02064B28
004E0277  addss    xmm1, xmm3
004E027B  movss    dword ptr [rip + 0x1b848a9], xmm5  ; -> 02064B2C
004E0283  movss    dword ptr [rip + 0x1b849d5], xmm0  ; -> 02064C60
004E028B  movaps   xmm0, xmm7
004E028E  mulss    xmm7, dword ptr [rip + 0x1b84a86]  ; -> 02064D1C
004E0296  mulss    xmm0, dword ptr [rip + 0x1b84a7a]  ; -> 02064D18
004E029E  addss    xmm7, xmm5
004E02A2  movss    dword ptr [rip + 0x1b849ba], xmm1  ; -> 02064C64
004E02AA  addss    xmm0, xmm4
004E02AE  ucomiss  xmm7, xmm9
004E02B2  movss    dword ptr [rip + 0x1b849ae], xmm0  ; -> 02064C68
004E02BA  movss    dword ptr [rip + 0x1b849aa], xmm7  ; -> 02064C6C
004E02C2  jp       0x4e02d2  ; -> 004E02D2
004E02C4  jne      0x4e02d2  ; -> 004E02D2
004E02C6  mov      dword ptr [rip + 0x1b84830], 0x7f7fffff  ; -> 02064B00
004E02D0  jmp      0x4e02e0  ; -> 004E02E0
004E02D2  divss    xmm8, xmm7
004E02D7  movss    dword ptr [rip + 0x1b84820], xmm8  ; -> 02064B00
004E02E0  movss    xmm3, dword ptr [rip + 0x1b849b8]  ; -> 02064CA0
004E02E8  movaps   xmm0, xmm10
004E02EC  movss    xmm2, dword ptr [rip + 0x1b849b0]  ; -> 02064CA4
004E02F4  addss    xmm0, xmm3
004E02F8  movaps   xmm1, xmm11
004E02FC  subss    xmm3, xmm10
004E0301  addss    xmm1, xmm2
004E0305  subss    xmm2, xmm11
004E030A  movss    dword ptr [rip + 0x1b8496e], xmm0  ; -> 02064C80
004E0312  ucomiss  xmm3, xmm9
004E0316  movss    xmm0, dword ptr [rip + 0x1b8498a]  ; -> 02064CA8
004E031E  movss    dword ptr [rip + 0x1b8495e], xmm1  ; -> 02064C84
004E0326  movss    xmm1, dword ptr [rip + 0x1b8497e]  ; -> 02064CAC
004E032E  movss    dword ptr [rip + 0x1b84962], xmm0  ; -> 02064C98
004E0336  movss    dword ptr [rip + 0x1b8495e], xmm1  ; -> 02064C9C
004E033E  movss    dword ptr [rip + 0x1b8494a], xmm3  ; -> 02064C90
004E0346  movss    dword ptr [rip + 0x1b84946], xmm2  ; -> 02064C94
004E034E  jp       0x4e0352  ; -> 004E0352
004E0350  je       0x4e035a  ; -> 004E035A
004E0352  ucomiss  xmm2, xmm9
004E0356  jp       0x4e036f  ; -> 004E036F
004E0358  jne      0x4e036f  ; -> 004E036F
004E035A  call     0x22cc40  ; -> 0022CC40 fn
004E035F  movss    xmm2, dword ptr [rip + 0x1b8492d]  ; -> 02064C94
004E0367  movss    xmm3, dword ptr [rip + 0x1b84921]  ; -> 02064C90
004E036F  comiss   xmm9, xmm3
004E0373  ja       0x4e037b  ; -> 004E037B
004E0375  comiss   xmm9, xmm2
004E0379  jbe      0x4e0380  ; -> 004E0380
004E037B  call     0x22cc30  ; -> 0022CC30 fn
004E0380  call     0x22cc20  ; -> 0022CC20 fn
004E0385  movss    xmm2, dword ptr [rip + 0x1b848f7]  ; -> 02064C84
004E038D  movss    xmm6, dword ptr [rip + 0x1b848eb]  ; -> 02064C80
004E0395  movaps   xmm0, xmm2
004E0398  mulss    xmm0, dword ptr [rip + 0x1b84950]  ; -> 02064CF0
004E03A0  movaps   xmm1, xmm2
004E03A3  movups   xmm7, xmmword ptr [rip + 0x1b84936]  ; -> 02064CE0
004E03AA  movss    xmm11, dword ptr [rip + 0x1b84949]  ; -> 02064CFC
004E03B3  movss    xmm14, dword ptr [rip + 0x1b84938]  ; -> 02064CF4
004E03BC  movss    xmm13, dword ptr [rip + 0x1b84933]  ; -> 02064CF8
004E03C5  movss    xmm15, dword ptr [rip + 0x1b84892]  ; -> 02064C60
004E03CE  movss    xmm8, dword ptr [rip + 0x1922465]  ; -> 01E0283C [f32 1]
004E03D7  mulss    xmm1, xmm13
004E03DC  shufps   xmm6, xmm6, 0
004E03E0  mulps    xmm6, xmm7
004E03E3  movups   xmmword ptr [rip + 0x1b84736], xmm6  ; -> 02064B20
004E03EA  movss    xmm5, dword ptr [rip + 0x1b8473a]  ; -> 02064B2C
004E03F2  addss    xmm6, xmm0
004E03F6  movss    xmm3, dword ptr [rip + 0x1b84726]  ; -> 02064B24
004E03FE  movaps   xmm0, xmm2
004E0401  movss    xmm4, dword ptr [rip + 0x1b8471f]  ; -> 02064B28
004E0409  mulss    xmm0, xmm14
004E040E  addss    xmm4, xmm1
004E0412  mulss    xmm2, xmm11
004E0417  addss    xmm3, xmm0
004E041B  addss    xmm5, xmm2
004E041F  movss    xmm2, dword ptr [rip + 0x1b84881]  ; -> 02064CA8
004E0427  movaps   xmm0, xmm2
004E042A  movaps   xmm1, xmm2
004E042D  mulss    xmm0, dword ptr [rip + 0x1b848cb]  ; -> 02064D00
004E0435  mulss    xmm1, dword ptr [rip + 0x1b848c7]  ; -> 02064D04
004E043D  addss    xmm6, xmm0
004E0441  movaps   xmm0, xmm2
004E0444  mulss    xmm0, dword ptr [rip + 0x1b848bc]  ; -> 02064D08
004E044C  mulss    xmm2, dword ptr [rip + 0x1b848b8]  ; -> 02064D0C
004E0454  addss    xmm3, xmm1
004E0458  addss    xmm4, xmm0
004E045C  addss    xmm5, xmm2
004E0460  movss    xmm2, dword ptr [rip + 0x1b84844]  ; -> 02064CAC
004E0468  movaps   xmm0, xmm2
004E046B  movaps   xmm1, xmm2
004E046E  mulss    xmm0, dword ptr [rip + 0x1b8489a]  ; -> 02064D10
004E0476  mulss    xmm1, dword ptr [rip + 0x1b84896]  ; -> 02064D14
004E047E  addss    xmm0, xmm6
004E0482  addss    xmm1, xmm3
004E0486  movss    dword ptr [rip + 0x1b847f2], xmm0  ; -> 02064C80
004E048E  movaps   xmm0, xmm2
004E0491  mulss    xmm0, dword ptr [rip + 0x1b8487f]  ; -> 02064D18
004E0499  mulss    xmm2, dword ptr [rip + 0x1b8487b]  ; -> 02064D1C
004E04A1  movss    dword ptr [rip + 0x1b847db], xmm1  ; -> 02064C84
004E04A9  addss    xmm0, xmm4
004E04AD  movss    xmm1, dword ptr [rip + 0x1b847af]  ; -> 02064C64
004E04B5  addss    xmm2, xmm5
004E04B9  movss    dword ptr [rip + 0x1b847c7], xmm0  ; -> 02064C88
004E04C1  movss    xmm0, dword ptr [rip + 0x1b84637]  ; -> 02064B00
004E04C9  ucomiss  xmm2, xmm9
004E04CD  mulss    xmm1, xmm0
004E04D1  mulss    xmm15, xmm0
004E04D6  movss    dword ptr [rsp + 0x110], xmm1
004E04DF  movss    xmm1, dword ptr [rip + 0x1b84781]  ; -> 02064C68
004E04E7  mulss    xmm1, xmm0
004E04EB  mulss    xmm0, xmm8
004E04F0  movss    dword ptr [rip + 0x1b84794], xmm2  ; -> 02064C8C
004E04F8  movss    dword ptr [rsp + 0x118], xmm1
004E0501  movss    dword ptr [rip + 0x1b84763], xmm0  ; -> 02064C6C
004E0509  jp       0x4e0518  ; -> 004E0518
004E050B  jne      0x4e0518  ; -> 004E0518
004E050D  movss    xmm10, dword ptr [rip + 0x41fe4a]  ; -> 00900360 [u32 0x7F7FFFFF]
004E0516  jmp      0x4e0521  ; -> 004E0521
004E0518  movaps   xmm10, xmm8
004E051C  divss    xmm10, xmm2
004E0521  movss    xmm2, dword ptr [rip + 0x1b8476b]  ; -> 02064C94
004E0529  movss    xmm6, dword ptr [rip + 0x1b8475f]  ; -> 02064C90
004E0531  movaps   xmm0, xmm2
004E0534  mulss    xmm0, dword ptr [rip + 0x1b847b4]  ; -> 02064CF0
004E053C  movaps   xmm1, xmm2
004E053F  mulss    xmm1, xmm13
004E0544  shufps   xmm6, xmm6, 0
004E0548  mulps    xmm6, xmm7
004E054B  movss    xmm7, dword ptr [rip + 0x1b84749]  ; -> 02064C9C
004E0553  movups   xmmword ptr [rip + 0x1b845c6], xmm6  ; -> 02064B20
004E055A  movss    xmm5, dword ptr [rip + 0x1b845ca]  ; -> 02064B2C
004E0562  addss    xmm6, xmm0
004E0566  movss    xmm3, dword ptr [rip + 0x1b845b6]  ; -> 02064B24
004E056E  movaps   xmm0, xmm2
004E0571  movss    xmm4, dword ptr [rip + 0x1b845af]  ; -> 02064B28
004E0579  mulss    xmm0, xmm14
004E057E  addss    xmm4, xmm1
004E0582  mulss    xmm2, xmm11
004E0587  addss    xmm3, xmm0
004E058B  addss    xmm5, xmm2
004E058F  movss    xmm2, dword ptr [rip + 0x1b84701]  ; -> 02064C98
004E0597  movaps   xmm0, xmm2
004E059A  movaps   xmm1, xmm2
004E059D  mulss    xmm0, dword ptr [rip + 0x1b8475b]  ; -> 02064D00
004E05A5  mulss    xmm1, dword ptr [rip + 0x1b84757]  ; -> 02064D04
004E05AD  addss    xmm6, xmm0
004E05B1  movaps   xmm0, xmm2
004E05B4  mulss    xmm0, dword ptr [rip + 0x1b8474c]  ; -> 02064D08
004E05BC  mulss    xmm2, dword ptr [rip + 0x1b84748]  ; -> 02064D0C
004E05C4  addss    xmm3, xmm1
004E05C8  addss    xmm4, xmm0
004E05CC  movss    dword ptr [rip + 0x1b8454c], xmm6  ; -> 02064B20
004E05D4  movaps   xmm0, xmm7
004E05D7  movaps   xmm1, xmm7
004E05DA  mulss    xmm0, dword ptr [rip + 0x1b8472e]  ; -> 02064D10
004E05E2  addss    xmm5, xmm2
004E05E6  mulss    xmm1, dword ptr [rip + 0x1b84726]  ; -> 02064D14
004E05EE  addss    xmm0, xmm6
004E05F2  movss    dword ptr [rip + 0x1b8452a], xmm3  ; -> 02064B24
004E05FA  movss    dword ptr [rip + 0x1b84526], xmm4  ; -> 02064B28
004E0602  addss    xmm1, xmm3
004E0606  movss    dword ptr [rip + 0x1b8451e], xmm5  ; -> 02064B2C
004E060E  movss    dword ptr [rip + 0x1b8467a], xmm0  ; -> 02064C90
004E0616  movaps   xmm0, xmm7
004E0619  mulss    xmm0, dword ptr [rip + 0x1b846f7]  ; -> 02064D18
004E0621  mulss    xmm7, dword ptr [rip + 0x1b846f3]  ; -> 02064D1C
004E0629  addss    xmm0, xmm4
004E062D  movss    dword ptr [rip + 0x1b8465f], xmm1  ; -> 02064C94
004E0635  movups   xmm1, xmmword ptr [rip + 0x1b84644]  ; -> 02064C80
004E063C  addss    xmm7, xmm5
004E0640  movss    dword ptr [rip + 0x1b84650], xmm0  ; -> 02064C98
004E0648  movaps   xmm0, xmm10
004E064C  shufps   xmm0, xmm0, 0
004E0650  mulps    xmm1, xmm0
004E0653  ucomiss  xmm7, xmm9
004E0657  mulss    xmm10, xmm8
004E065C  movups   xmmword ptr [rip + 0x1b8461d], xmm1  ; -> 02064C80
004E0663  movss    dword ptr [rip + 0x1b84620], xmm10  ; -> 02064C8C
004E066C  movss    dword ptr [rip + 0x1b84628], xmm7  ; -> 02064C9C
004E0674  jp       0x4e0682  ; -> 004E0682
004E0676  jne      0x4e0682  ; -> 004E0682
004E0678  movss    xmm2, dword ptr [rip + 0x41fce0]  ; -> 00900360 [u32 0x7F7FFFFF]
004E0680  jmp      0x4e068a  ; -> 004E068A
004E0682  movaps   xmm2, xmm8
004E0686  divss    xmm2, xmm7
004E068A  movups   xmm1, xmmword ptr [rip + 0x1b845ff]  ; -> 02064C90
004E0691  movss    xmm10, dword ptr [rip + 0x1b84496]  ; -> 02064B30
004E069A  movaps   xmm0, xmm2
004E069D  movss    xmm5, dword ptr [rip + 0x1b845db]  ; -> 02064C80
004E06A5  ucomiss  xmm10, xmm5
004E06A9  shufps   xmm0, xmm0, 0
004E06AD  mulps    xmm1, xmm0
004E06B0  movss    dword ptr [rip + 0x1b84448], xmm2  ; -> 02064B00
004E06B8  mulss    xmm2, xmm8
004E06BD  movups   xmmword ptr [rip + 0x1b845cc], xmm1  ; -> 02064C90
004E06C4  movss    dword ptr [rip + 0x1b845d0], xmm2  ; -> 02064C9C
004E06CC  jp       0x4e06d8  ; -> 004E06D8
004E06CE  jne      0x4e06d8  ; -> 004E06D8
004E06D0  mov      r9d, 1
004E06D6  jmp      0x4e06db  ; -> 004E06DB
004E06D8  xor      r9d, r9d
004E06DB  movss    xmm7, dword ptr [rip + 0x1b84451]  ; -> 02064B34
004E06E3  movss    xmm4, dword ptr [rip + 0x1b84599]  ; -> 02064C84
004E06EB  ucomiss  xmm7, xmm4
004E06EE  jp       0x4e06fa  ; -> 004E06FA
004E06F0  jne      0x4e06fa  ; -> 004E06FA
004E06F2  mov      r8d, 1
004E06F8  jmp      0x4e06fd  ; -> 004E06FD
004E06FA  xor      r8d, r8d
004E06FD  movss    xmm1, dword ptr [rip + 0x1b84433]  ; -> 02064B38
004E0705  movss    xmm3, dword ptr [rip + 0x1b8457b]  ; -> 02064C88
004E070D  ucomiss  xmm1, xmm3
004E0710  jp       0x4e071b  ; -> 004E071B
004E0712  jne      0x4e071b  ; -> 004E071B
004E0714  mov      edx, 1
004E0719  jmp      0x4e071d  ; -> 004E071D
004E071B  xor      edx, edx
004E071D  movzx    edi, word ptr [rip + 0x1b846b0]  ; -> 02064DD4
004E0724  xor      ecx, ecx
004E0726  movss    xmm14, dword ptr [rip + 0x1922101]  ; -> 01E02830 [u32 0x00000000]
004E072F  comiss   xmm5, xmm10
004E0733  seta     cl
004E0736  xor      eax, eax
004E0738  add      cx, cx
004E073B  comiss   xmm4, xmm7
004E073E  seta     al
004E0741  add      cx, ax
004E0744  xor      eax, eax
004E0746  add      cx, cx
004E0749  comiss   xmm3, xmm1
004E074C  seta     al
004E074F  dec      di
004E0752  add      cx, ax
004E0755  mov      word ptr [rip + 0x1b84678], di  ; -> 02064DD4
004E075C  shl      cx, 2
004E0760  add      cx, r9w
004E0764  add      cx, cx
004E0767  add      cx, r8w
004E076B  add      cx, cx
004E076E  add      cx, dx
004E0771  add      cx, cx
004E0774  ucomiss  xmm5, xmm14
004E0778  mov      word ptr [rip + 0x1b84391], cx  ; -> 02064B10
004E077F  jp       0x4e078b  ; -> 004E078B
004E0781  jne      0x4e078b  ; -> 004E078B
004E0783  mov      r10d, 1
004E0789  jmp      0x4e078e  ; -> 004E078E
004E078B  xor      r10d, r10d
004E078E  movss    xmm13, dword ptr [rip + 0x192209d]  ; -> 01E02834 [u32 0x00000000]
004E0797  ucomiss  xmm4, xmm13
004E079B  jp       0x4e07a7  ; -> 004E07A7
004E079D  jne      0x4e07a7  ; -> 004E07A7
004E079F  mov      r9d, 1
004E07A5  jmp      0x4e07aa  ; -> 004E07AA
004E07A7  xor      r9d, r9d
004E07AA  movss    xmm11, dword ptr [rip + 0x1922085]  ; -> 01E02838 [u32 0x00000000]
004E07B3  ucomiss  xmm3, xmm11
004E07B7  jp       0x4e07c2  ; -> 004E07C2
004E07B9  jne      0x4e07c2  ; -> 004E07C2
004E07BB  mov      edx, 1
004E07C0  jmp      0x4e07c4  ; -> 004E07C4
004E07C2  xor      edx, edx
004E07C4  movss    xmm6, dword ptr [rip + 0x1b844c4]  ; -> 02064C90
004E07CC  xor      r8d, r8d
004E07CF  comiss   xmm14, xmm5
004E07D3  seta     r8b
004E07D7  xor      eax, eax
004E07D9  add      r8w, r8w
004E07DD  comiss   xmm13, xmm4
004E07E1  seta     al
004E07E4  add      r8w, ax
004E07E8  xor      eax, eax
004E07EA  add      r8w, r8w
004E07EE  comiss   xmm11, xmm3
004E07F2  seta     al
004E07F5  add      r8w, ax
004E07F9  shl      r8w, 2
004E07FE  add      r8w, r10w
004E0802  add      r8w, r8w
004E0806  add      r8w, r9w
004E080A  add      r8w, r8w
004E080E  add      r8w, dx
004E0812  add      r8w, r8w
004E0816  ucomiss  xmm10, xmm6
004E081A  mov      word ptr [rip + 0x1b842f0], r8w  ; -> 02064B12
004E0822  jp       0x4e082e  ; -> 004E082E
004E0824  jne      0x4e082e  ; -> 004E082E
004E0826  mov      r10d, 1
004E082C  jmp      0x4e0831  ; -> 004E0831
004E082E  xor      r10d, r10d
004E0831  movss    xmm2, dword ptr [rip + 0x1b8445b]  ; -> 02064C94
004E0839  ucomiss  xmm7, xmm2
004E083C  jp       0x4e0848  ; -> 004E0848
004E083E  jne      0x4e0848  ; -> 004E0848
004E0840  mov      r9d, 1
004E0846  jmp      0x4e084b  ; -> 004E084B
004E0848  xor      r9d, r9d
004E084B  movss    xmm0, dword ptr [rip + 0x1b84445]  ; -> 02064C98
004E0853  ucomiss  xmm1, xmm0
004E0856  jp       0x4e0861  ; -> 004E0861
004E0858  jne      0x4e0861  ; -> 004E0861
004E085A  mov      edx, 1
004E085F  jmp      0x4e0863  ; -> 004E0863
004E0861  xor      edx, edx
004E0863  xor      ebx, ebx
004E0865  comiss   xmm6, xmm10
004E0869  seta     bl
004E086C  xor      eax, eax
004E086E  add      bx, bx
004E0871  comiss   xmm2, xmm7
004E0874  seta     al
004E0877  add      bx, ax
004E087A  xor      eax, eax
004E087C  add      bx, bx
004E087F  comiss   xmm0, xmm1
004E0882  seta     al
004E0885  add      bx, ax
004E0888  shl      bx, 2
004E088C  add      bx, r10w
004E0890  add      bx, bx
004E0893  add      bx, r9w
004E0897  add      bx, bx
004E089A  add      bx, dx
004E089D  add      bx, bx
004E08A0  ucomiss  xmm6, xmm14
004E08A4  mov      word ptr [rip + 0x1b84269], bx  ; -> 02064B14
004E08AB  jp       0x4e08b7  ; -> 004E08B7
004E08AD  jne      0x4e08b7  ; -> 004E08B7
004E08AF  mov      r11d, 1
004E08B5  jmp      0x4e08ba  ; -> 004E08BA
004E08B7  xor      r11d, r11d
004E08BA  ucomiss  xmm2, xmm13
004E08BE  jp       0x4e08ca  ; -> 004E08CA
004E08C0  jne      0x4e08ca  ; -> 004E08CA
004E08C2  mov      r9d, 1
004E08C8  jmp      0x4e08cd  ; -> 004E08CD
004E08CA  xor      r9d, r9d
004E08CD  ucomiss  xmm0, xmm11
004E08D1  jp       0x4e08dc  ; -> 004E08DC
004E08D3  jne      0x4e08dc  ; -> 004E08DC
004E08D5  mov      edx, 1
004E08DA  jmp      0x4e08de  ; -> 004E08DE
004E08DC  xor      edx, edx
004E08DE  movss    xmm1, dword ptr [rip + 0x1b84322]  ; -> 02064C08
004E08E6  xor      r10d, r10d
004E08E9  movzx    esi, word ptr [rip + 0x1b8421c]  ; -> 02064B0C
004E08F0  addss    xmm1, dword ptr [rip + 0x1b84314]  ; -> 02064C0C
004E08F8  comiss   xmm14, xmm6
004E08FC  mulss    xmm3, xmm12
004E0901  seta     r10b
004E0905  mulss    xmm5, xmm12
004E090A  xor      eax, eax
004E090C  add      r10w, r10w
004E0910  mulss    xmm4, xmm12
004E0915  comiss   xmm13, xmm2
004E0919  mulss    xmm15, xmm12
004E091E  seta     al
004E0921  mulss    xmm6, xmm12
004E0926  add      r10w, ax
004E092A  xor      eax, eax
004E092C  add      r10w, r10w
004E0930  mulss    xmm2, xmm12
004E0935  comiss   xmm11, xmm0
004E0939  mulss    xmm0, xmm12
004E093E  seta     al
004E0941  movss    dword ptr [rip + 0x1b842bf], xmm1  ; -> 02064C08
004E0949  add      r10w, ax
004E094D  shl      r10w, 2
004E0952  add      r10w, r11w
004E0956  add      r10w, r10w
004E095A  add      r10w, r9w
004E095E  lea      r9d, [rsi + rbp]
004E0962  cvttss2si eax, xmm5
004E0966  add      r10w, r10w
004E096A  movzx    r11d, r9w
004E096E  add      r10w, dx
004E0972  and      r11w, cx
004E0976  movzx    edx, r9w
004E097A  movzx    ecx, r9w
004E097E  and      dx, r8w
004E0982  add      r10w, r10w
004E0986  and      r9w, r10w
004E098A  mov      word ptr [rip + 0x1b8444f], dx  ; -> 02064DE0
004E0991  and      cx, bx
004E0994  mov      word ptr [rip + 0x1b8444c], r9w  ; -> 02064DE8
004E099C  mov      word ptr [rip + 0x1b84441], cx  ; -> 02064DE4
004E09A3  mov      dword ptr [rip + 0x1b842d7], eax  ; -> 02064C80
004E09A9  cvttss2si eax, xmm4
004E09AD  mov      word ptr [rip + 0x1b84161], r10w  ; -> 02064B16
004E09B5  mov      dword ptr [rip + 0x1b842c9], eax  ; -> 02064C84
004E09BB  cvttss2si eax, xmm3
004E09BF  movss    xmm3, dword ptr [rsp + 0x110]
004E09C8  mov      dword ptr [rip + 0x1b842ba], eax  ; -> 02064C88
004E09CE  mulss    xmm3, xmm12
004E09D3  cvttss2si eax, xmm15
004E09D8  mov      dword ptr [rip + 0x1b84282], eax  ; -> 02064C60
004E09DE  cvttss2si eax, xmm3
004E09E2  movss    xmm3, dword ptr [rsp + 0x118]
004E09EB  mov      dword ptr [rip + 0x1b84273], eax  ; -> 02064C64
004E09F1  cvttss2si eax, xmm6
004E09F5  mulss    xmm3, xmm12
004E09FA  mov      dword ptr [rip + 0x1b84290], eax  ; -> 02064C90
004E0A00  cvttss2si eax, xmm2
004E0A04  cvttss2si r8d, xmm3
004E0A09  mov      dword ptr [rip + 0x1b84285], eax  ; -> 02064C94
004E0A0F  cvttss2si eax, xmm0
004E0A13  mov      dword ptr [rip + 0x1b8424e], r8d  ; -> 02064C68
004E0A1A  movsd    xmm0, qword ptr [rip + 0x1b8423e]  ; -> 02064C60
004E0A22  mov      dword ptr [rip + 0x1b84270], eax  ; -> 02064C98
004E0A28  movsx    eax, dx
004E0A2B  movsx    edx, cx
004E0A2E  add      dx, ax
004E0A31  movsx    ecx, r9w
004E0A35  movsx    r9d, word ptr [rip + 0x1b8439b]  ; -> 02064DD8
004E0A3D  add      dx, cx
004E0A40  add      r11w, dx
004E0A44  mov      word ptr [rip + 0x1b84390], r11w  ; -> 02064DDC
004E0A4C  lea      eax, [r9 + 0x100]
004E0A53  shl      eax, 4
004E0A56  movsxd   r10, eax
004E0A59  lea      eax, [r9 + 0x180]
004E0A60  shl      eax, 4
004E0A63  movsd    qword ptr [r10 + r15], xmm0
004E0A69  mov      dword ptr [r10 + r15 + 8], r8d
004E0A6E  movups   xmm0, xmmword ptr [rip + 0x1b8421b]  ; -> 02064C90
004E0A75  movsxd   rcx, eax
004E0A78  lea      eax, [r9 + 0x80]
004E0A7F  shl      eax, 4
004E0A82  movups   xmmword ptr [rcx + r15], xmm0
004E0A87  movsxd   rcx, eax
004E0A8A  mov      dword ptr [r10 + r15 + 0xc], esi
004E0A8F  movups   xmm0, xmmword ptr [rip + 0x1b841ea]  ; -> 02064C80
004E0A96  movups   xmmword ptr [rcx + r15], xmm0
004E0A9B  cmp      r11w, si
004E0A9F  je       0x4e0aad  ; -> 004E0AAD
004E0AA1  movzx    eax, word ptr [rip + 0x1b84318]  ; -> 02064DC0
004E0AA8  mov      dword ptr [r10 + r15 + 0xc], eax
004E0AAD  inc      r9w
004E0AB1  mov      word ptr [rip + 0x1b8431f], r9w  ; -> 02064DD8
004E0AB9  cmp      si, di
004E0ABC  jne      0x4e0120  ; -> 004E0120
004E0AC2  movsx    edx, si
004E0AC5  lea      eax, [rdx + 0xa]
004E0AC8  shl      eax, 4
004E0ACB  movsxd   r8, eax
004E0ACE  lea      eax, [rdx + 0xb]
004E0AD1  shl      eax, 4
004E0AD4  movsxd   r9, eax
004E0AD7  lea      eax, [rdx + 0xc]
004E0ADA  shl      eax, 4
004E0ADD  movups   xmm0, xmmword ptr [r8 + r15]
004E0AE2  movsxd   r11, eax
004E0AE5  lea      eax, [rdx + 0xd]
004E0AE8  movups   xmm2, xmmword ptr [r9 + r15]
004E0AED  shl      eax, 4
004E0AF0  movsxd   rsi, eax
004E0AF3  lea      eax, [rdx + 0xe]
004E0AF6  movups   xmm3, xmmword ptr [r11 + r15]
004E0AFB  shl      eax, 4
004E0AFE  movsxd   r14, eax
004E0B01  lea      eax, [rdx + 0xf]
004E0B04  movups   xmm4, xmmword ptr [rsi + r15]
004E0B09  shl      eax, 4
004E0B0C  cvtdq2ps xmm6, xmm0
004E0B0F  movsxd   rbp, eax
004E0B12  lea      eax, [rdx + 0x10]
004E0B15  shl      eax, 4
004E0B18  movsxd   rdi, eax
004E0B1B  lea      eax, [rdx + 0x11]
004E0B1E  shl      eax, 4
004E0B21  movups   xmm0, xmmword ptr [r14 + r15]
004E0B26  movsxd   rbx, eax
004E0B29  lea      eax, [rdx + 0x12]
004E0B2C  movups   xmm5, xmmword ptr [r15 + rbp]
004E0B31  shl      eax, 4
004E0B34  movdqu   xmmword ptr [rip + 0x1b83ff4], xmm6  ; -> 02064B30
004E0B3C  movsxd   r10, eax
004E0B3F  lea      eax, [rdx + 2]
004E0B42  movss    xmm1, dword ptr [rip + 0x1b83fee]  ; -> 02064B38
004E0B4A  cvtdq2ps xmm9, xmm0
004E0B4E  shl      eax, 4
004E0B51  movsxd   rcx, eax
004E0B54  movups   xmm0, xmmword ptr [r10 + r15]
004E0B59  movups   xmm11, xmmword ptr [rcx + r15]
004E0B5E  cvtdq2ps xmm10, xmm0
004E0B62  movss    xmm0, dword ptr [rip + 0x1b83fc6]  ; -> 02064B30
004E0B6A  cvtdq2ps xmm7, xmm2
004E0B6D  movups   xmm2, xmmword ptr [rbx + r15]
004E0B72  movdqu   xmmword ptr [rip + 0x1b83fc6], xmm7  ; -> 02064B40
004E0B7A  cvtdq2ps xmm8, xmm3
004E0B7E  movups   xmm3, xmmword ptr [rdi + r15]
004E0B83  movups   xmmword ptr [rip + 0x1b84035], xmm11  ; -> 02064BC0
004E0B8B  shufps   xmm11, xmm11, 0x55
004E0B90  mulss    xmm0, xmm11
004E0B95  mulss    xmm1, xmm11
004E0B9A  movss    dword ptr [rip + 0x1b83f8e], xmm0  ; -> 02064B30
004E0BA2  movss    xmm0, dword ptr [rip + 0x1b83f92]  ; -> 02064B3C
004E0BAA  mulss    xmm0, xmm11
004E0BAF  movss    dword ptr [rip + 0x1b83f81], xmm1  ; -> 02064B38
004E0BB7  movss    xmm1, dword ptr [rip + 0x1b83f89]  ; -> 02064B48
004E0BBF  movss    dword ptr [rip + 0x1b83f75], xmm0  ; -> 02064B3C
004E0BC7  movss    xmm0, dword ptr [rip + 0x1b83f71]  ; -> 02064B40
004E0BCF  cvtdq2ps xmm4, xmm4
004E0BD2  cvtdq2ps xmm5, xmm5
004E0BD5  cvtdq2ps xmm3, xmm3
004E0BD8  cvtdq2ps xmm2, xmm2
004E0BDB  shufps   xmm6, xmm6, 0x55
004E0BDF  shufps   xmm7, xmm7, 0x55
004E0BE3  mulss    xmm0, xmm11
004E0BE8  mulss    xmm6, xmm11
004E0BED  mulss    xmm7, xmm11
004E0BF2  movss    dword ptr [rip + 0x1b83f46], xmm0  ; -> 02064B40
004E0BFA  movss    dword ptr [rip + 0x1b83f32], xmm6  ; -> 02064B34
004E0C02  movss    dword ptr [rip + 0x1b83f3a], xmm7  ; -> 02064B44
004E0C0A  movdqu   xmmword ptr [rip + 0x1b83f3d], xmm8  ; -> 02064B50
004E0C13  movdqu   xmmword ptr [rip + 0x1b83f45], xmm4  ; -> 02064B60
004E0C1B  movdqu   xmmword ptr [rip + 0x1b83f4c], xmm9  ; -> 02064B70
004E0C24  movdqu   xmmword ptr [rip + 0x1b83f54], xmm5  ; -> 02064B80
004E0C2C  movdqu   xmmword ptr [rip + 0x1b83f5c], xmm3  ; -> 02064B90
004E0C34  movdqu   xmmword ptr [rip + 0x1b83f64], xmm2  ; -> 02064BA0
004E0C3C  movdqu   xmmword ptr [rip + 0x1b83f6b], xmm10  ; -> 02064BB0
004E0C45  mulss    xmm1, xmm11
004E0C4A  movss    xmm0, dword ptr [rip + 0x1b83efa]  ; -> 02064B4C
004E0C52  lea      eax, [rdx + 4]
004E0C55  mulss    xmm0, xmm11
004E0C5A  shl      eax, 4
004E0C5D  movss    dword ptr [rip + 0x1b83ee3], xmm1  ; -> 02064B48
004E0C65  movss    xmm1, dword ptr [rip + 0x1b83eeb]  ; -> 02064B58
004E0C6D  movss    dword ptr [rip + 0x1b83ed7], xmm0  ; -> 02064B4C
004E0C75  movss    xmm0, dword ptr [rip + 0x1b83ed3]  ; -> 02064B50
004E0C7D  mulss    xmm0, xmm11
004E0C82  movsxd   rcx, eax
004E0C85  mulss    xmm1, xmm11
004E0C8A  movss    dword ptr [rip + 0x1b83ebe], xmm0  ; -> 02064B50
004E0C92  movss    xmm0, dword ptr [rip + 0x1b83ec2]  ; -> 02064B5C
004E0C9A  mulss    xmm0, xmm11
004E0C9F  movss    dword ptr [rip + 0x1b83eb1], xmm1  ; -> 02064B58
004E0CA7  movss    xmm1, dword ptr [rip + 0x1b83eb9]  ; -> 02064B68
004E0CAF  movss    dword ptr [rip + 0x1b83ea5], xmm0  ; -> 02064B5C
004E0CB7  movss    xmm0, dword ptr [rip + 0x1b83ea1]  ; -> 02064B60
004E0CBF  mulss    xmm0, xmm11
004E0CC4  mulss    xmm1, xmm11
004E0CC9  movss    dword ptr [rip + 0x1b83e8f], xmm0  ; -> 02064B60
004E0CD1  movss    xmm0, dword ptr [rip + 0x1b83e93]  ; -> 02064B6C
004E0CD9  mulss    xmm0, xmm11
004E0CDE  movss    dword ptr [rip + 0x1b83e82], xmm1  ; -> 02064B68
004E0CE6  movss    xmm1, dword ptr [rip + 0x1b83e8a]  ; -> 02064B78
004E0CEE  movss    dword ptr [rip + 0x1b83e76], xmm0  ; -> 02064B6C
004E0CF6  movups   xmm0, xmmword ptr [rcx + r15]
004E0CFB  mulss    xmm1, xmm11
004E0D00  movups   xmmword ptr [rip + 0x1b83ef9], xmm0  ; -> 02064C00
004E0D07  movss    xmm0, dword ptr [rip + 0x1b83e61]  ; -> 02064B70
004E0D0F  mulss    xmm0, xmm11
004E0D14  movss    dword ptr [rip + 0x1b83e5c], xmm1  ; -> 02064B78
004E0D1C  movss    xmm1, dword ptr [rip + 0x1b83e64]  ; -> 02064B88
004E0D24  movss    dword ptr [rip + 0x1b83e44], xmm0  ; -> 02064B70
004E0D2C  movss    xmm0, dword ptr [rip + 0x1b83e48]  ; -> 02064B7C
004E0D34  mulss    xmm0, xmm11
004E0D39  mulss    xmm1, xmm11
004E0D3E  movss    dword ptr [rip + 0x1b83e36], xmm0  ; -> 02064B7C
004E0D46  movups   xmm0, xmmword ptr [rip + 0x1b83de3]  ; -> 02064B30
004E0D4D  movss    dword ptr [rip + 0x1b83e33], xmm1  ; -> 02064B88
004E0D55  movss    xmm1, dword ptr [rip + 0x1b83e3b]  ; -> 02064B98
004E0D5D  movups   xmmword ptr [r8 + r15], xmm0
004E0D62  movss    xmm0, dword ptr [rip + 0x1b83e16]  ; -> 02064B80
004E0D6A  mulss    xmm0, xmm11
004E0D6F  shufps   xmm8, xmm8, 0x55
004E0D74  mulss    xmm8, xmm11
004E0D79  movss    dword ptr [rip + 0x1b83dff], xmm0  ; -> 02064B80
004E0D81  movss    xmm0, dword ptr [rip + 0x1b83e03]  ; -> 02064B8C
004E0D89  mulss    xmm0, xmm11
004E0D8E  movss    dword ptr [rip + 0x1b83dbd], xmm8  ; -> 02064B54
004E0D97  shufps   xmm4, xmm4, 0x55
004E0D9B  movss    dword ptr [rip + 0x1b83de9], xmm0  ; -> 02064B8C
004E0DA3  movups   xmm0, xmmword ptr [rip + 0x1b83d96]  ; -> 02064B40
004E0DAA  shufps   xmm9, xmm9, 0x55
004E0DAF  movups   xmmword ptr [r9 + r15], xmm0
004E0DB4  movss    xmm0, dword ptr [rip + 0x1b83dd4]  ; -> 02064B90
004E0DBC  mulss    xmm0, xmm11
004E0DC1  shufps   xmm5, xmm5, 0x55
004E0DC5  shufps   xmm3, xmm3, 0x55
004E0DC9  movss    dword ptr [rip + 0x1b83dbf], xmm0  ; -> 02064B90
004E0DD1  movss    xmm0, dword ptr [rip + 0x1b83dc3]  ; -> 02064B9C
004E0DD9  mulss    xmm0, xmm11
004E0DDE  shufps   xmm2, xmm2, 0x55
004E0DE2  mulss    xmm4, xmm11
004E0DE7  movss    dword ptr [rip + 0x1b83dad], xmm0  ; -> 02064B9C
004E0DEF  movups   xmm0, xmmword ptr [rip + 0x1b83d5a]  ; -> 02064B50
004E0DF6  mulss    xmm9, xmm11
004E0DFB  movups   xmmword ptr [r11 + r15], xmm0
004E0E00  movss    xmm0, dword ptr [rip + 0x1b83d98]  ; -> 02064BA0
004E0E08  mulss    xmm0, xmm11
004E0E0D  mulss    xmm5, xmm11
004E0E12  mulss    xmm3, xmm11
004E0E17  mulss    xmm1, xmm11
004E0E1C  mulss    xmm2, xmm11
004E0E21  movss    dword ptr [rip + 0x1b83d77], xmm0  ; -> 02064BA0
004E0E29  movss    dword ptr [rip + 0x1b83d33], xmm4  ; -> 02064B64
004E0E31  movss    dword ptr [rip + 0x1b83d3a], xmm9  ; -> 02064B74
004E0E3A  movss    dword ptr [rip + 0x1b83d42], xmm5  ; -> 02064B84
004E0E42  movss    dword ptr [rip + 0x1b83d4a], xmm3  ; -> 02064B94
004E0E4A  movss    dword ptr [rip + 0x1b83d46], xmm1  ; -> 02064B98
004E0E52  movss    dword ptr [rip + 0x1b83d4a], xmm2  ; -> 02064BA4
004E0E5A  movss    xmm0, dword ptr [rip + 0x1b83d4a]  ; -> 02064BAC
004E0E62  lea      r11, [rsp + 0xc0]
004E0E6A  movss    xmm1, dword ptr [rip + 0x1b83d36]  ; -> 02064BA8
004E0E72  movaps   xmm6, xmmword ptr [r11 - 0x10]
004E0E77  movaps   xmm7, xmmword ptr [r11 - 0x20]
004E0E7C  movaps   xmm8, xmmword ptr [r11 - 0x30]
004E0E81  movaps   xmm9, xmmword ptr [r11 - 0x40]
004E0E86  movaps   xmm12, xmmword ptr [r11 - 0x70]
004E0E8B  movaps   xmm13, xmmword ptr [r11 - 0x80]
004E0E90  movaps   xmm14, xmmword ptr [rsp + 0x30]
004E0E96  movaps   xmm15, xmmword ptr [rsp + 0x20]
004E0E9C  mulss    xmm0, xmm11
004E0EA1  mulss    xmm1, xmm11
004E0EA6  movss    dword ptr [rip + 0x1b83cfe], xmm0  ; -> 02064BAC
004E0EAE  movups   xmm0, xmmword ptr [rip + 0x1b83cab]  ; -> 02064B60
004E0EB5  movss    dword ptr [rip + 0x1b83ceb], xmm1  ; -> 02064BA8
004E0EBD  movss    xmm1, dword ptr [rip + 0x1b83cf3]  ; -> 02064BB8
004E0EC5  movups   xmmword ptr [rsi + r15], xmm0
004E0ECA  movss    xmm0, dword ptr [rip + 0x1b83cde]  ; -> 02064BB0
004E0ED2  mulss    xmm0, xmm11
004E0ED7  mulss    xmm1, xmm11
004E0EDC  movss    dword ptr [rip + 0x1b83ccc], xmm0  ; -> 02064BB0
004E0EE4  movss    xmm0, dword ptr [rip + 0x1b83cd0]  ; -> 02064BBC
004E0EEC  mulss    xmm0, xmm11
004E0EF1  movss    dword ptr [rip + 0x1b83cbf], xmm1  ; -> 02064BB8
004E0EF9  movups   xmm1, xmmword ptr [rip + 0x1b83c80]  ; -> 02064B80
004E0F00  movss    dword ptr [rip + 0x1b83cb4], xmm0  ; -> 02064BBC
004E0F08  movups   xmm0, xmmword ptr [rip + 0x1b83c61]  ; -> 02064B70
004E0F0F  shufps   xmm10, xmm10, 0x55
004E0F14  movups   xmmword ptr [r14 + r15], xmm0
004E0F19  movups   xmm0, xmmword ptr [rip + 0x1b83c70]  ; -> 02064B90
004E0F20  movups   xmmword ptr [r15 + rbp], xmm1
004E0F25  movups   xmm1, xmmword ptr [rip + 0x1b83c74]  ; -> 02064BA0
004E0F2C  mulss    xmm10, xmm11
004E0F31  movaps   xmm11, xmmword ptr [r11 - 0x60]
004E0F36  movups   xmmword ptr [rdi + r15], xmm0
004E0F3B  movss    dword ptr [rip + 0x1b83c70], xmm10  ; -> 02064BB4
004E0F44  movups   xmm0, xmmword ptr [rip + 0x1b83c65]  ; -> 02064BB0
004E0F4B  movaps   xmm10, xmmword ptr [r11 - 0x50]
004E0F50  movups   xmmword ptr [rbx + r15], xmm1
004E0F55  mov      rbx, qword ptr [r11 + 0x40]
004E0F59  movups   xmmword ptr [r10 + r15], xmm0
004E0F5E  mov      rsp, r11
004E0F61  pop      r15
004E0F63  pop      r14
004E0F65  pop      r13
004E0F67  pop      r12
004E0F69  pop      rdi
004E0F6A  pop      rsi
004E0F6B  pop      rbp
004E0F6C  ret      
```

## 004E0F70 (6587 B, extent 004E0F70-004E292B)

Page context: " the 77 rows the [VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md)'s template census decodes; §2.4b there reads the rest of this chain and gives the map — type ''h'' installs '004DF440' and '004E0F70', ''i'' installs '004DCC00' and '004DDDF0', '0xA3' installs '004DB350', '0xA6' and '0xA8' share '004DA8A0', and ''j'' installs '004D7BF0'. **The copied template carries the MPG descriptor verbatim**, which is how the program reache"

```
004E0F70  mov      rax, rsp
004E0F73  push     rbx
004E0F74  push     rbp
004E0F75  push     rsi
004E0F76  push     rdi
004E0F77  push     r12
004E0F79  push     r14
004E0F7B  push     r15
004E0F7D  sub      rsp, 0xe0
004E0F84  movaps   xmmword ptr [rax - 0x48], xmm6
004E0F88  lea      r12, [rip + 0x1b83ea1]  ; -> 02064E30
004E0F8F  movaps   xmmword ptr [rax - 0x58], xmm7
004E0F93  mov      r15, rcx
004E0F96  movaps   xmmword ptr [rax - 0x68], xmm8
004E0F9B  xor      r8d, r8d
004E0F9E  movaps   xmmword ptr [rax - 0x78], xmm9
004E0FA3  mov      r14, rdx
004E0FA6  movaps   xmmword ptr [rax - 0x88], xmm10
004E0FAE  movaps   xmmword ptr [rax - 0x98], xmm11
004E0FB6  movzx    eax, word ptr [rip + 0x1b83b4f]  ; -> 02064B0C
004E0FBD  add      ax, 0x2b
004E0FC1  movaps   xmmword ptr [rsp + 0x70], xmm12
004E0FC7  mov      word ptr [rip + 0x1b83e06], ax  ; -> 02064DD4
004E0FCE  cwde     
004E0FCF  shl      eax, 4
004E0FD2  movsxd   rcx, eax
004E0FD5  movaps   xmmword ptr [rsp + 0x60], xmm13
004E0FDB  add      rcx, r12
004E0FDE  movaps   xmmword ptr [rsp + 0x50], xmm14
004E0FE4  movaps   xmmword ptr [rsp + 0x40], xmm15
004E0FEA  call     r15
004E0FED  movsx    r8d, word ptr [rip + 0x1b83b17]  ; -> 02064B0C
004E0FF5  xorps    xmm6, xmm6
004E0FF8  movss    xmm4, dword ptr [rip + 0x1921830]  ; -> 01E02830 [u32 0x00000000]
004E1000  mov      edx, r8d
004E1003  movss    xmm2, dword ptr [rip + 0x192182d]  ; -> 01E02838 [u32 0x00000000]
004E100B  movaps   xmm13, xmm4
004E100F  movss    xmm14, dword ptr [rip + 0x1921824]  ; -> 01E0283C [f32 1]
004E1018  movss    xmm10, dword ptr [rip + 0x1921813]  ; -> 01E02834 [u32 0x00000000]
004E1021  lea      eax, [r8 + 0x2a]
004E1025  movss    xmm12, dword ptr [rip + 0x41f332]  ; -> 00900360 [u32 0x7F7FFFFF]
004E102E  addss    xmm2, xmm14
004E1033  shl      eax, 4
004E1036  movsxd   rcx, eax
004E1039  lea      eax, [r8 + 3]
004E103D  shl      eax, 4
004E1040  movups   xmm11, xmmword ptr [rcx + r12]
004E1045  movsxd   rcx, eax
004E1048  lea      eax, [r8 + 0x29]
004E104C  shl      eax, 4
004E104F  movups   xmmword ptr [rip + 0x1b83b79], xmm11  ; -> 02064BD0
004E1057  movups   xmm1, xmmword ptr [rcx + r12]
004E105C  movsxd   rcx, eax
004E105F  lea      eax, [r8 + 2]
004E1063  shl      eax, 4
004E1066  movups   xmmword ptr [rip + 0x1b83b83], xmm1  ; -> 02064BF0
004E106D  movups   xmm5, xmmword ptr [rcx + r12]
004E1072  movsxd   rcx, eax
004E1075  shufps   xmm11, xmm11, 0xaa
004E107A  addss    xmm13, xmm11
004E107F  shufps   xmm1, xmm1, 0xff
004E1083  addss    xmm1, xmm4
004E1087  movss    xmm0, dword ptr [rcx + r12]
004E108D  subss    xmm2, xmm11
004E1092  movss    dword ptr [rip + 0x1b83bb6], xmm0  ; -> 02064C50
004E109A  movss    xmm0, dword ptr [rip + 0x1b83b56]  ; -> 02064BF8
004E10A2  ucomiss  xmm13, xmm6
004E10A6  addss    xmm0, xmm10
004E10AB  movss    dword ptr [rip + 0x1b83b2c], xmm13  ; -> 02064BE0
004E10B4  movss    dword ptr [rip + 0x1b83b34], xmm1  ; -> 02064BF0
004E10BC  movss    dword ptr [rip + 0x1b83b24], xmm2  ; -> 02064BE8
004E10C4  movss    dword ptr [rip + 0x1b83b28], xmm0  ; -> 02064BF4
004E10CC  jp       0x4e10d6  ; -> 004E10D6
004E10CE  jne      0x4e10d6  ; -> 004E10D6
004E10D0  movaps   xmm3, xmm12
004E10D4  jmp      0x4e10df  ; -> 004E10DF
004E10D6  movaps   xmm3, xmm14
004E10DA  divss    xmm3, xmm13
004E10DF  movss    xmm0, dword ptr [rip + 0x3e4a4d]  ; -> 008C5B34 [f32 0.0078125]
004E10E7  mov      eax, edx
004E10E9  shl      eax, 4
004E10EC  movaps   xmm9, xmm10
004E10F0  movsxd   rcx, eax
004E10F3  addss    xmm10, xmm3
004E10F8  movss    dword ptr [rip + 0x1b83a04], xmm0  ; -> 02064B04
004E1100  addss    xmm9, xmm4
004E1105  cvtdq2ps xmm1, xmm5
004E1108  movzx    eax, word ptr [rcx + r12 + 0xc]
004E110E  mov      word ptr [rip + 0x1b83cb3], ax  ; -> 02064DC8
004E1115  lea      eax, [r8 + rdx]
004E1119  mov      word ptr [rip + 0x1b83cac], ax  ; -> 02064DCC
004E1120  lea      eax, [rdx + 0xa]
004E1123  shl      eax, 4
004E1126  mulps    xmm1, xmmword ptr [rip + 0x8415e3]  ; -> 00D22710 [f32x4 0.0078125, 0.0078125, 0.0078125, 0.0078125]
004E112D  movsxd   rcx, eax
004E1130  lea      eax, [rdx + 0xb]
004E1133  shl      eax, 4
004E1136  movss    dword ptr [rip + 0x1b839c2], xmm3  ; -> 02064B00
004E113E  movss    dword ptr [rip + 0x1b83b0d], xmm9  ; -> 02064C54
004E1147  movups   xmm0, xmmword ptr [rcx + r12]
004E114C  movsxd   rcx, eax
004E114F  lea      eax, [rdx + 0xc]
004E1152  shl      eax, 4
004E1155  movups   xmmword ptr [rip + 0x1b839d4], xmm0  ; -> 02064B30
004E115C  movups   xmm0, xmmword ptr [rcx + r12]
004E1161  movsxd   rcx, eax
004E1164  lea      eax, [rdx + 0xd]
004E1167  shl      eax, 4
004E116A  ucomiss  xmm10, xmm6
004E116E  movups   xmmword ptr [rip + 0x1b839cb], xmm0  ; -> 02064B40
004E1175  movups   xmm0, xmmword ptr [rcx + r12]
004E117A  movsxd   rcx, eax
004E117D  movss    dword ptr [rip + 0x1b83a5e], xmm10  ; -> 02064BE4
004E1186  movups   xmmword ptr [rip + 0x1b839c3], xmm0  ; -> 02064B50
004E118D  movups   xmm0, xmmword ptr [rcx + r12]
004E1192  movups   xmmword ptr [rip + 0x1b83a27], xmm1  ; -> 02064BC0
004E1199  movups   xmmword ptr [rip + 0x1b839c0], xmm0  ; -> 02064B60
004E11A0  jp       0x4e11e6  ; -> 004E11E6
004E11A2  jne      0x4e11e6  ; -> 004E11E6
004E11A4  call     0x22cc40  ; -> 0022CC40 fn
004E11A9  movzx    r8d, word ptr [rip + 0x1b8395b]  ; -> 02064B0C
004E11B1  movss    xmm2, dword ptr [rip + 0x1b83a2f]  ; -> 02064BE8
004E11B9  movss    xmm11, dword ptr [rip + 0x1b83a16]  ; -> 02064BD8
004E11C2  movss    xmm9, dword ptr [rip + 0x1b83a89]  ; -> 02064C54
004E11CB  movss    xmm14, dword ptr [rip + 0x1921668]  ; -> 01E0283C [f32 1]
004E11D4  movss    xmm10, dword ptr [rip + 0x1b83a07]  ; -> 02064BE4
004E11DD  movss    xmm13, dword ptr [rip + 0x1b839fa]  ; -> 02064BE0
004E11E6  comiss   xmm6, xmm10
004E11EA  jbe      0x4e122e  ; -> 004E122E
004E11EC  call     0x22cc30  ; -> 0022CC30 fn
004E11F1  movzx    r8d, word ptr [rip + 0x1b83913]  ; -> 02064B0C
004E11F9  movss    xmm2, dword ptr [rip + 0x1b839e7]  ; -> 02064BE8
004E1201  movss    xmm11, dword ptr [rip + 0x1b839ce]  ; -> 02064BD8
004E120A  movss    xmm9, dword ptr [rip + 0x1b83a41]  ; -> 02064C54
004E1213  movss    xmm14, dword ptr [rip + 0x1921620]  ; -> 01E0283C [f32 1]
004E121C  movss    xmm10, dword ptr [rip + 0x1b839bf]  ; -> 02064BE4
004E1225  movss    xmm13, dword ptr [rip + 0x1b839b2]  ; -> 02064BE0
004E122E  ucomiss  xmm2, xmm6
004E1231  jp       0x4e1235  ; -> 004E1235
004E1233  je       0x4e123e  ; -> 004E123E
004E1235  movaps   xmm12, xmm14
004E1239  divss    xmm12, xmm2
004E123E  movss    xmm5, dword ptr [rip + 0x1b8397a]  ; -> 02064BC0
004E1246  movss    xmm6, dword ptr [rip + 0x1b83976]  ; -> 02064BC4
004E124E  movss    xmm7, dword ptr [rip + 0x1b83972]  ; -> 02064BC8
004E1256  movss    xmm8, dword ptr [rip + 0x1b8396d]  ; -> 02064BCC
004E125F  movss    xmm0, dword ptr [rip + 0x1b838c9]  ; -> 02064B30
004E1267  movss    xmm1, dword ptr [rip + 0x1b838d1]  ; -> 02064B40
004E126F  movss    xmm15, dword ptr [rip + 0x1b838e8]  ; -> 02064B60
004E1278  mulss    xmm0, xmm5
004E127C  movsx    edx, r8w
004E1280  mulss    xmm1, xmm5
004E1284  movss    dword ptr [rip + 0x1b838a4], xmm0  ; -> 02064B30
004E128C  movss    xmm0, dword ptr [rip + 0x1b838a0]  ; -> 02064B34
004E1294  lea      eax, [rdx + 0xe]
004E1297  mulss    xmm0, xmm6
004E129B  shl      eax, 4
004E129E  movsxd   rcx, eax
004E12A1  lea      eax, [rdx + 0xf]
004E12A4  movss    dword ptr [rip + 0x1b83894], xmm1  ; -> 02064B40
004E12AC  movss    xmm1, dword ptr [rip + 0x1b83894]  ; -> 02064B48
004E12B4  movss    dword ptr [rip + 0x1b83878], xmm0  ; -> 02064B34
004E12BC  movups   xmm2, xmmword ptr [rcx + r12]
004E12C1  shl      eax, 4
004E12C4  movss    xmm0, dword ptr [rip + 0x1b8386c]  ; -> 02064B38
004E12CC  mulss    xmm0, xmm7
004E12D0  movsxd   rcx, eax
004E12D3  lea      eax, [rdx + 0x10]
004E12D6  mulss    xmm1, xmm7
004E12DA  shl      eax, 4
004E12DD  movss    dword ptr [rip + 0x1b83853], xmm0  ; -> 02064B38
004E12E5  movss    xmm0, dword ptr [rip + 0x1b8384f]  ; -> 02064B3C
004E12ED  movups   xmm4, xmmword ptr [rcx + r12]
004E12F2  movsxd   rcx, eax
004E12F5  lea      eax, [rdx + 0x11]
004E12F8  mulss    xmm0, xmm8
004E12FD  shl      eax, 4
004E1300  movss    dword ptr [rip + 0x1b83840], xmm1  ; -> 02064B48
004E1308  movss    xmm1, dword ptr [rip + 0x1b83840]  ; -> 02064B50
004E1310  movss    dword ptr [rip + 0x1b83824], xmm0  ; -> 02064B3C
004E1318  movss    xmm0, dword ptr [rip + 0x1b83824]  ; -> 02064B44
004E1320  mulss    xmm0, xmm6
004E1324  mulss    xmm1, xmm5
004E1328  movss    dword ptr [rip + 0x1b83814], xmm0  ; -> 02064B44
004E1330  movss    xmm0, dword ptr [rip + 0x1b83814]  ; -> 02064B4C
004E1338  mulss    xmm0, xmm8
004E133D  movups   xmmword ptr [rip + 0x1b8382c], xmm2  ; -> 02064B70
004E1344  movss    dword ptr [rip + 0x1b83800], xmm0  ; -> 02064B4C
004E134C  movss    xmm0, dword ptr [rip + 0x1b83800]  ; -> 02064B54
004E1354  mulss    xmm0, xmm6
004E1358  movss    dword ptr [rip + 0x1b837f0], xmm1  ; -> 02064B50
004E1360  movss    xmm1, dword ptr [rip + 0x1b837f0]  ; -> 02064B58
004E1368  movss    dword ptr [rip + 0x1b837e4], xmm0  ; -> 02064B54
004E1370  movss    xmm0, dword ptr [rip + 0x1b837e4]  ; -> 02064B5C
004E1378  mulss    xmm0, xmm8
004E137D  mulss    xmm1, xmm7
004E1381  movss    dword ptr [rip + 0x1b837d3], xmm0  ; -> 02064B5C
004E1389  movups   xmm0, xmmword ptr [rcx + r12]
004E138E  movsxd   rcx, eax
004E1391  mulss    xmm15, xmm5
004E1396  movups   xmmword ptr [rsp + 0x30], xmm0
004E139B  movups   xmm3, xmmword ptr [rcx + r12]
004E13A0  movups   xmmword ptr [rip + 0x1b837e9], xmm0  ; -> 02064B90
004E13A7  movss    xmm0, dword ptr [rip + 0x1b837b5]  ; -> 02064B64
004E13AF  mulss    xmm0, xmm6
004E13B3  mulss    xmm2, xmm5
004E13B7  movss    dword ptr [rsp + 0x120], xmm0
004E13C0  movss    dword ptr [rip + 0x1b8379c], xmm0  ; -> 02064B64
004E13C8  movss    xmm0, dword ptr [rip + 0x1b83798]  ; -> 02064B68
004E13D0  mulss    xmm0, xmm7
004E13D4  movss    dword ptr [rip + 0x1b83723], xmm12  ; -> 02064B00
004E13DD  movss    dword ptr [rip + 0x1b83773], xmm1  ; -> 02064B58
004E13E5  movss    dword ptr [rsp + 0x130], xmm0
004E13EE  movss    dword ptr [rip + 0x1b83772], xmm0  ; -> 02064B68
004E13F6  movss    xmm0, dword ptr [rip + 0x1b8376e]  ; -> 02064B6C
004E13FE  mulss    xmm0, xmm8
004E1403  movss    dword ptr [rip + 0x1b83754], xmm15  ; -> 02064B60
004E140C  movss    dword ptr [rip + 0x1b8375c], xmm2  ; -> 02064B70
004E1414  movss    dword ptr [rsp + 0x138], xmm0
004E141D  movss    dword ptr [rip + 0x1b83747], xmm0  ; -> 02064B6C
004E1425  movss    xmm0, dword ptr [rip + 0x1b83747]  ; -> 02064B74
004E142D  movups   xmmword ptr [rip + 0x1b8374c], xmm4  ; -> 02064B80
004E1434  movups   xmmword ptr [rip + 0x1b83765], xmm3  ; -> 02064BA0
004E143B  movss    xmm1, dword ptr [rip + 0x1b83735]  ; -> 02064B78
004E1443  lea      eax, [rdx + 0x12]
004E1446  mulss    xmm0, xmm6
004E144A  shl      eax, 4
004E144D  mulss    xmm1, xmm7
004E1451  movsxd   rcx, eax
004E1454  mov      eax, 0x2bc
004E1459  movss    dword ptr [rip + 0x1b83713], xmm0  ; -> 02064B74
004E1461  add      eax, r8d
004E1464  movss    xmm0, dword ptr [rip + 0x1b83710]  ; -> 02064B7C
004E146C  mulss    xmm0, xmm8
004E1471  mov      word ptr [rip + 0x1b83938], ax  ; -> 02064DB0
004E1478  inc      ax
004E147B  ucomiss  xmm11, xmm9
004E147F  mov      word ptr [rip + 0x1b8392e], ax  ; -> 02064DB4
004E1486  mov      word ptr [rip + 0x1b8392a], r8w  ; -> 02064DB8
004E148E  mov      word ptr [rip + 0x1b8393a], r8w  ; -> 02064DD0
004E1496  movups   xmm2, xmmword ptr [rcx + r12]
004E149B  movss    dword ptr [rip + 0x1b836d9], xmm0  ; -> 02064B7C
004E14A3  movss    xmm0, dword ptr [rip + 0x1b836d9]  ; -> 02064B84
004E14AB  mulss    xmm0, xmm6
004E14AF  movups   xmmword ptr [rip + 0x1b836fa], xmm2  ; -> 02064BB0
004E14B6  movss    dword ptr [rip + 0x1b836c6], xmm0  ; -> 02064B84
004E14BE  movss    xmm0, dword ptr [rip + 0x1b836c6]  ; -> 02064B8C
004E14C6  mulss    xmm0, xmm8
004E14CB  movss    dword ptr [rip + 0x1b836a5], xmm1  ; -> 02064B78
004E14D3  movss    xmm1, dword ptr [rip + 0x1b836ad]  ; -> 02064B88
004E14DB  movss    dword ptr [rip + 0x1b836a9], xmm0  ; -> 02064B8C
004E14E3  movss    xmm0, dword ptr [rip + 0x1b836a9]  ; -> 02064B94
004E14EB  mulss    xmm0, xmm6
004E14EF  mulss    xmm1, xmm7
004E14F3  movss    dword ptr [rsp + 0x20], xmm0
004E14F9  movss    dword ptr [rip + 0x1b83693], xmm0  ; -> 02064B94
004E1501  movss    xmm0, dword ptr [rip + 0x1b8368f]  ; -> 02064B98
004E1509  mulss    xmm0, xmm7
004E150D  movss    dword ptr [rip + 0x1b83673], xmm1  ; -> 02064B88
004E1515  movss    xmm1, dword ptr [rip + 0x1b8368b]  ; -> 02064BA8
004E151D  movss    dword ptr [rsp + 0x24], xmm0
004E1523  movss    dword ptr [rip + 0x1b8366d], xmm0  ; -> 02064B98
004E152B  movss    xmm0, dword ptr [rip + 0x1b83669]  ; -> 02064B9C
004E1533  mulss    xmm0, xmm8
004E1538  mulss    xmm4, xmm5
004E153C  movss    dword ptr [rsp + 0x28], xmm0
004E1542  movss    dword ptr [rip + 0x1b83652], xmm0  ; -> 02064B9C
004E154A  movss    xmm0, dword ptr [rip + 0x1b83652]  ; -> 02064BA4
004E1552  mulss    xmm0, xmm6
004E1556  mulss    xmm1, xmm7
004E155A  movss    dword ptr [rip + 0x1b83642], xmm0  ; -> 02064BA4
004E1562  movss    xmm0, dword ptr [rip + 0x1b83642]  ; -> 02064BAC
004E156A  mulss    xmm0, xmm8
004E156F  movss    dword ptr [rip + 0x1b83609], xmm4  ; -> 02064B80
004E1577  movups   xmm4, xmmword ptr [rsp + 0x30]
004E157C  movss    dword ptr [rip + 0x1b83628], xmm0  ; -> 02064BAC
004E1584  movss    xmm0, dword ptr [rip + 0x1b83628]  ; -> 02064BB4
004E158C  mulss    xmm0, xmm6
004E1590  movss    dword ptr [rip + 0x1b83610], xmm1  ; -> 02064BA8
004E1598  movss    xmm1, dword ptr [rip + 0x1b83618]  ; -> 02064BB8
004E15A0  movss    dword ptr [rip + 0x1b8360c], xmm0  ; -> 02064BB4
004E15A8  movss    xmm0, dword ptr [rip + 0x1b8360c]  ; -> 02064BBC
004E15B0  mulss    xmm0, xmm8
004E15B5  mulss    xmm4, xmm5
004E15B9  mulss    xmm3, xmm5
004E15BD  mulss    xmm2, xmm5
004E15C1  mulss    xmm1, xmm7
004E15C5  mulss    xmm12, xmm14
004E15CA  movss    dword ptr [rip + 0x1b835ea], xmm0  ; -> 02064BBC
004E15D2  movss    dword ptr [rip + 0x1b835b6], xmm4  ; -> 02064B90
004E15DA  movss    dword ptr [rip + 0x1b835be], xmm3  ; -> 02064BA0
004E15E2  movss    dword ptr [rip + 0x1b835c6], xmm2  ; -> 02064BB0
004E15EA  movss    dword ptr [rip + 0x1b835c6], xmm1  ; -> 02064BB8
004E15F2  movss    dword ptr [rip + 0x1b835f1], xmm12  ; -> 02064BEC
004E15FB  jp       0x4e1606  ; -> 004E1606
004E15FD  jne      0x4e1606  ; -> 004E1606
004E15FF  mov      eax, 1
004E1604  jmp      0x4e1608  ; -> 004E1608
004E1606  xor      eax, eax
004E1608  xor      ecx, ecx
004E160A  mov      word ptr [rip + 0x1b837aa], r8w  ; -> 02064DBC
004E1612  comiss   xmm9, xmm11
004E1616  seta     cl
004E1619  shl      cx, 4
004E161D  add      cx, ax
004E1620  lea      eax, [r8 + 0x20]
004E1624  add      cx, cx
004E1627  and      ax, cx
004E162A  mov      word ptr [rip + 0x1b834df], cx  ; -> 02064B10
004E1631  mov      word ptr [rip + 0x1b837ac], ax  ; -> 02064DE4
004E1638  cmp      ax, r8w
004E163C  jne      0x4e1888  ; -> 004E1888
004E1642  movss    xmm0, dword ptr [rsp + 0x120]
004E164B  subss    xmm0, dword ptr [rip + 0x1b834e1]  ; -> 02064B34
004E1653  movss    xmm1, dword ptr [rsp + 0x130]
004E165C  subss    xmm15, dword ptr [rip + 0x1b834cb]  ; -> 02064B30
004E1665  subss    xmm1, dword ptr [rip + 0x1b834cb]  ; -> 02064B38
004E166D  mulss    xmm10, xmm9
004E1672  movss    dword ptr [rip + 0x1b835fa], xmm0  ; -> 02064C74
004E167A  movss    xmm0, dword ptr [rsp + 0x138]
004E1683  subss    xmm0, dword ptr [rip + 0x1b834b1]  ; -> 02064B3C
004E168B  movss    dword ptr [rip + 0x1b835b0], xmm10  ; -> 02064C44
004E1694  movss    dword ptr [rip + 0x1b835d3], xmm15  ; -> 02064C70
004E169D  movss    dword ptr [rip + 0x1b835d3], xmm1  ; -> 02064C78
004E16A5  movss    dword ptr [rip + 0x1b835cf], xmm0  ; -> 02064C7C
004E16AD  call     0x22cc20  ; -> 0022CC20 fn
004E16B2  movss    xmm0, dword ptr [rip + 0x1b834b6]  ; -> 02064B70
004E16BA  subss    xmm0, dword ptr [rip + 0x1b8347e]  ; -> 02064B40
004E16C2  movss    xmm1, dword ptr [rip + 0x1b834aa]  ; -> 02064B74
004E16CA  subss    xmm1, dword ptr [rip + 0x1b83472]  ; -> 02064B44
004E16D2  movss    dword ptr [rip + 0x1b835a6], xmm0  ; -> 02064C80
004E16DA  movss    xmm0, dword ptr [rip + 0x1b83496]  ; -> 02064B78
004E16E2  subss    xmm0, dword ptr [rip + 0x1b8345e]  ; -> 02064B48
004E16EA  movss    dword ptr [rip + 0x1b83592], xmm1  ; -> 02064C84
004E16F2  movss    xmm1, dword ptr [rip + 0x1b83482]  ; -> 02064B7C
004E16FA  subss    xmm1, dword ptr [rip + 0x1b8344a]  ; -> 02064B4C
004E1702  movss    dword ptr [rip + 0x1b8357e], xmm0  ; -> 02064C88
004E170A  movss    dword ptr [rip + 0x1b8357a], xmm1  ; -> 02064C8C
004E1712  call     0x22cc20  ; -> 0022CC20 fn
004E1717  movss    xmm0, dword ptr [rip + 0x1b83461]  ; -> 02064B80
004E171F  subss    xmm0, dword ptr [rip + 0x1b83429]  ; -> 02064B50
004E1727  movss    xmm1, dword ptr [rip + 0x1b83455]  ; -> 02064B84
004E172F  subss    xmm1, dword ptr [rip + 0x1b8341d]  ; -> 02064B54
004E1737  movss    dword ptr [rip + 0x1b83551], xmm0  ; -> 02064C90
004E173F  movss    xmm0, dword ptr [rip + 0x1b83441]  ; -> 02064B88
004E1747  subss    xmm0, dword ptr [rip + 0x1b83409]  ; -> 02064B58
004E174F  movss    dword ptr [rip + 0x1b8353d], xmm1  ; -> 02064C94
004E1757  movss    xmm1, dword ptr [rip + 0x1b8342d]  ; -> 02064B8C
004E175F  subss    xmm1, dword ptr [rip + 0x1b833f5]  ; -> 02064B5C
004E1767  movss    dword ptr [rip + 0x1b83529], xmm0  ; -> 02064C98
004E176F  movss    dword ptr [rip + 0x1b83525], xmm1  ; -> 02064C9C
004E1777  call     0x22cc20  ; -> 0022CC20 fn
004E177C  movss    xmm0, dword ptr [rip + 0x1b834c0]  ; -> 02064C44
004E1784  movss    xmm2, dword ptr [rip + 0x1b834e8]  ; -> 02064C74
004E178C  movss    xmm1, dword ptr [rip + 0x1b834dc]  ; -> 02064C70
004E1794  movss    xmm3, dword ptr [rip + 0x1b834dc]  ; -> 02064C78
004E179C  movss    xmm4, dword ptr [rip + 0x1b834d8]  ; -> 02064C7C
004E17A4  movss    xmm5, dword ptr [rip + 0x1b834d4]  ; -> 02064C80
004E17AC  movss    xmm6, dword ptr [rip + 0x1b834d0]  ; -> 02064C84
004E17B4  movss    xmm7, dword ptr [rip + 0x1b834cc]  ; -> 02064C88
004E17BC  movss    xmm8, dword ptr [rip + 0x1b834c7]  ; -> 02064C8C
004E17C5  movss    xmm11, dword ptr [rip + 0x1b834c6]  ; -> 02064C94
004E17CE  movss    xmm10, dword ptr [rip + 0x1b834b9]  ; -> 02064C90
004E17D7  movss    xmm12, dword ptr [rip + 0x1b834b8]  ; -> 02064C98
004E17E0  movss    xmm13, dword ptr [rip + 0x1b834b3]  ; -> 02064C9C
004E17E9  mulss    xmm2, xmm0
004E17ED  mulss    xmm1, xmm0
004E17F1  addss    xmm2, dword ptr [rip + 0x1b8333b]  ; -> 02064B34
004E17F9  mulss    xmm3, xmm0
004E17FD  addss    xmm1, dword ptr [rip + 0x1b8332b]  ; -> 02064B30
004E1805  mulss    xmm4, xmm0
004E1809  addss    xmm3, dword ptr [rip + 0x1b83327]  ; -> 02064B38
004E1811  mulss    xmm6, xmm0
004E1815  addss    xmm4, dword ptr [rip + 0x1b8331f]  ; -> 02064B3C
004E181D  mulss    xmm5, xmm0
004E1821  addss    xmm6, dword ptr [rip + 0x1b8331b]  ; -> 02064B44
004E1829  mulss    xmm7, xmm0
004E182D  addss    xmm5, dword ptr [rip + 0x1b8330b]  ; -> 02064B40
004E1835  mulss    xmm8, xmm0
004E183A  addss    xmm7, dword ptr [rip + 0x1b83306]  ; -> 02064B48
004E1842  mulss    xmm11, xmm0
004E1847  addss    xmm8, dword ptr [rip + 0x1b832fc]  ; -> 02064B4C
004E1850  mulss    xmm10, xmm0
004E1855  addss    xmm11, dword ptr [rip + 0x1b832f6]  ; -> 02064B54
004E185E  mulss    xmm12, xmm0
004E1863  addss    xmm10, dword ptr [rip + 0x1b832e4]  ; -> 02064B50
004E186C  mulss    xmm13, xmm0
004E1871  addss    xmm12, dword ptr [rip + 0x1b832de]  ; -> 02064B58
004E187A  addss    xmm13, dword ptr [rip + 0x1b832d9]  ; -> 02064B5C
004E1883  jmp      0x4e1ac3  ; -> 004E1AC3
004E1888  movss    xmm1, dword ptr [rsp + 0x20]
004E188E  subss    xmm4, xmm15
004E1893  subss    xmm1, dword ptr [rsp + 0x120]
004E189C  movss    xmm0, dword ptr [rsp + 0x24]
004E18A2  subss    xmm9, xmm13
004E18A7  subss    xmm0, dword ptr [rsp + 0x130]
004E18B0  movss    dword ptr [rip + 0x1b833b8], xmm4  ; -> 02064C70
004E18B8  movss    dword ptr [rip + 0x1b833b4], xmm1  ; -> 02064C74
004E18C0  movss    xmm1, dword ptr [rsp + 0x28]
004E18C6  subss    xmm1, dword ptr [rsp + 0x138]
004E18CF  mulss    xmm9, xmm12
004E18D4  movss    dword ptr [rip + 0x1b8339c], xmm0  ; -> 02064C78
004E18DC  movss    dword ptr [rip + 0x1b83398], xmm1  ; -> 02064C7C
004E18E4  movss    dword ptr [rip + 0x1b83357], xmm9  ; -> 02064C44
004E18ED  call     0x22cc20  ; -> 0022CC20 fn
004E18F2  movss    xmm0, dword ptr [rip + 0x1b832a6]  ; -> 02064BA0
004E18FA  subss    xmm0, dword ptr [rip + 0x1b8326e]  ; -> 02064B70
004E1902  movss    xmm1, dword ptr [rip + 0x1b8329a]  ; -> 02064BA4
004E190A  subss    xmm1, dword ptr [rip + 0x1b83262]  ; -> 02064B74
004E1912  movss    dword ptr [rip + 0x1b83366], xmm0  ; -> 02064C80
004E191A  movss    xmm0, dword ptr [rip + 0x1b83286]  ; -> 02064BA8
004E1922  subss    xmm0, dword ptr [rip + 0x1b8324e]  ; -> 02064B78
004E192A  movss    dword ptr [rip + 0x1b83352], xmm1  ; -> 02064C84
004E1932  movss    xmm1, dword ptr [rip + 0x1b83272]  ; -> 02064BAC
004E193A  subss    xmm1, dword ptr [rip + 0x1b8323a]  ; -> 02064B7C
004E1942  movss    dword ptr [rip + 0x1b8333e], xmm0  ; -> 02064C88
004E194A  movss    dword ptr [rip + 0x1b8333a], xmm1  ; -> 02064C8C
004E1952  call     0x22cc20  ; -> 0022CC20 fn
004E1957  movss    xmm0, dword ptr [rip + 0x1b83251]  ; -> 02064BB0
004E195F  subss    xmm0, dword ptr [rip + 0x1b83219]  ; -> 02064B80
004E1967  movss    xmm1, dword ptr [rip + 0x1b83245]  ; -> 02064BB4
004E196F  subss    xmm1, dword ptr [rip + 0x1b8320d]  ; -> 02064B84
004E1977  movss    dword ptr [rip + 0x1b83311], xmm0  ; -> 02064C90
004E197F  movss    xmm0, dword ptr [rip + 0x1b83231]  ; -> 02064BB8
004E1987  subss    xmm0, dword ptr [rip + 0x1b831f9]  ; -> 02064B88
004E198F  movss    dword ptr [rip + 0x1b832fd], xmm1  ; -> 02064C94
004E1997  movss    xmm1, dword ptr [rip + 0x1b8321d]  ; -> 02064BBC
004E199F  subss    xmm1, dword ptr [rip + 0x1b831e5]  ; -> 02064B8C
004E19A7  movss    dword ptr [rip + 0x1b832e9], xmm0  ; -> 02064C98
004E19AF  movss    dword ptr [rip + 0x1b832e5], xmm1  ; -> 02064C9C
004E19B7  call     0x22cc20  ; -> 0022CC20 fn
004E19BC  movss    xmm0, dword ptr [rip + 0x1b83280]  ; -> 02064C44
004E19C4  movss    xmm2, dword ptr [rip + 0x1b832a8]  ; -> 02064C74
004E19CC  movss    xmm1, dword ptr [rip + 0x1b8329c]  ; -> 02064C70
004E19D4  movss    xmm3, dword ptr [rip + 0x1b8329c]  ; -> 02064C78
004E19DC  movss    xmm4, dword ptr [rip + 0x1b83298]  ; -> 02064C7C
004E19E4  movss    xmm5, dword ptr [rip + 0x1b83294]  ; -> 02064C80
004E19EC  movss    xmm6, dword ptr [rip + 0x1b83290]  ; -> 02064C84
004E19F4  movss    xmm7, dword ptr [rip + 0x1b8328c]  ; -> 02064C88
004E19FC  movss    xmm8, dword ptr [rip + 0x1b83287]  ; -> 02064C8C
004E1A05  movss    xmm11, dword ptr [rip + 0x1b83286]  ; -> 02064C94
004E1A0E  movss    xmm10, dword ptr [rip + 0x1b83279]  ; -> 02064C90
004E1A17  movss    xmm12, dword ptr [rip + 0x1b83278]  ; -> 02064C98
004E1A20  movss    xmm13, dword ptr [rip + 0x1b83273]  ; -> 02064C9C
004E1A29  mulss    xmm2, xmm0
004E1A2D  mulss    xmm1, xmm0
004E1A31  addss    xmm2, dword ptr [rip + 0x1b8312b]  ; -> 02064B64
004E1A39  mulss    xmm3, xmm0
004E1A3D  addss    xmm1, dword ptr [rip + 0x1b8311b]  ; -> 02064B60
004E1A45  mulss    xmm4, xmm0
004E1A49  addss    xmm3, dword ptr [rip + 0x1b83117]  ; -> 02064B68
004E1A51  mulss    xmm6, xmm0
004E1A55  addss    xmm4, dword ptr [rip + 0x1b8310f]  ; -> 02064B6C
004E1A5D  mulss    xmm5, xmm0
004E1A61  addss    xmm6, dword ptr [rip + 0x1b8310b]  ; -> 02064B74
004E1A69  mulss    xmm7, xmm0
004E1A6D  addss    xmm5, dword ptr [rip + 0x1b830fb]  ; -> 02064B70
004E1A75  mulss    xmm8, xmm0
004E1A7A  addss    xmm7, dword ptr [rip + 0x1b830f6]  ; -> 02064B78
004E1A82  mulss    xmm11, xmm0
004E1A87  addss    xmm8, dword ptr [rip + 0x1b830ec]  ; -> 02064B7C
004E1A90  mulss    xmm10, xmm0
004E1A95  addss    xmm11, dword ptr [rip + 0x1b830e6]  ; -> 02064B84
004E1A9E  mulss    xmm12, xmm0
004E1AA3  addss    xmm10, dword ptr [rip + 0x1b830d4]  ; -> 02064B80
004E1AAC  mulss    xmm13, xmm0
004E1AB1  addss    xmm12, dword ptr [rip + 0x1b830ce]  ; -> 02064B88
004E1ABA  addss    xmm13, dword ptr [rip + 0x1b830c9]  ; -> 02064B8C
004E1AC3  movss    xmm9, dword ptr [rip + 0x3e4074]  ; -> 008C5B40 [f32 255]
004E1ACC  comiss   xmm9, xmm1
004E1AD0  movss    dword ptr [rip + 0x1b831c3], xmm13  ; -> 02064C9C
004E1AD9  movss    dword ptr [rip + 0x1b831b6], xmm12  ; -> 02064C98
004E1AE2  movss    dword ptr [rip + 0x1b831a9], xmm11  ; -> 02064C94
004E1AEB  movss    dword ptr [rip + 0x1b8319c], xmm10  ; -> 02064C90
004E1AF4  movss    dword ptr [rip + 0x1b8318f], xmm8  ; -> 02064C8C
004E1AFD  movss    dword ptr [rip + 0x1b83183], xmm7  ; -> 02064C88
004E1B05  movss    dword ptr [rip + 0x1b83177], xmm6  ; -> 02064C84
004E1B0D  movss    dword ptr [rip + 0x1b8316b], xmm5  ; -> 02064C80
004E1B15  movss    dword ptr [rip + 0x1b8315f], xmm4  ; -> 02064C7C
004E1B1D  movss    dword ptr [rip + 0x1b83153], xmm3  ; -> 02064C78
004E1B25  movss    dword ptr [rip + 0x1b83147], xmm2  ; -> 02064C74
004E1B2D  movss    dword ptr [rip + 0x1b8313b], xmm1  ; -> 02064C70
004E1B35  ja       0x4e1b41  ; -> 004E1B41
004E1B37  mov      dword ptr [rip + 0x1b8312f], 0x437f0000  ; -> 02064C70
004E1B41  comiss   xmm9, xmm2
004E1B45  ja       0x4e1b51  ; -> 004E1B51
004E1B47  mov      dword ptr [rip + 0x1b83123], 0x437f0000  ; -> 02064C74
004E1B51  comiss   xmm9, xmm3
004E1B55  ja       0x4e1b61  ; -> 004E1B61
004E1B57  mov      dword ptr [rip + 0x1b83117], 0x437f0000  ; -> 02064C78
004E1B61  comiss   xmm9, xmm4
004E1B65  ja       0x4e1b71  ; -> 004E1B71
004E1B67  mov      dword ptr [rip + 0x1b8310b], 0x437f0000  ; -> 02064C7C
004E1B71  comiss   xmm9, xmm5
004E1B75  ja       0x4e1b81  ; -> 004E1B81
004E1B77  mov      dword ptr [rip + 0x1b830ff], 0x437f0000  ; -> 02064C80
004E1B81  comiss   xmm9, xmm6
004E1B85  ja       0x4e1b91  ; -> 004E1B91
004E1B87  mov      dword ptr [rip + 0x1b830f3], 0x437f0000  ; -> 02064C84
004E1B91  comiss   xmm9, xmm7
004E1B95  ja       0x4e1ba1  ; -> 004E1BA1
004E1B97  mov      dword ptr [rip + 0x1b830e7], 0x437f0000  ; -> 02064C88
004E1BA1  comiss   xmm9, xmm8
004E1BA5  ja       0x4e1bb1  ; -> 004E1BB1
004E1BA7  mov      dword ptr [rip + 0x1b830db], 0x437f0000  ; -> 02064C8C
004E1BB1  comiss   xmm9, xmm10
004E1BB5  ja       0x4e1bc1  ; -> 004E1BC1
004E1BB7  mov      dword ptr [rip + 0x1b830cf], 0x437f0000  ; -> 02064C90
004E1BC1  comiss   xmm9, xmm11
004E1BC5  ja       0x4e1bd1  ; -> 004E1BD1
004E1BC7  mov      dword ptr [rip + 0x1b830c3], 0x437f0000  ; -> 02064C94
004E1BD1  comiss   xmm9, xmm12
004E1BD5  ja       0x4e1be1  ; -> 004E1BE1
004E1BD7  mov      dword ptr [rip + 0x1b830b7], 0x437f0000  ; -> 02064C98
004E1BE1  comiss   xmm9, xmm13
004E1BE5  ja       0x4e1bf1  ; -> 004E1BF1
004E1BE7  mov      dword ptr [rip + 0x1b830ab], 0x437f0000  ; -> 02064C9C
004E1BF1  movss    xmm4, dword ptr [rip + 0x1920c3b]  ; -> 01E02834 [u32 0x00000000]
004E1BF9  movsx    edx, word ptr [rip + 0x1b831bc]  ; -> 02064DBC
004E1C00  movups   xmm1, xmmword ptr [rip + 0x1b83079]  ; -> 02064C80
004E1C07  mov      dword ptr [rip + 0x1b82ef3], 0x3f000000  ; -> 02064B04
004E1C11  movups   xmm0, xmmword ptr [rip + 0x1b83058]  ; -> 02064C70
004E1C18  lea      eax, [rdx + 0x80]
004E1C1E  movss    xmm5, dword ptr [rip + 0x1920c12]  ; -> 01E02838 [u32 0x00000000]
004E1C26  addss    xmm5, dword ptr [rip + 0x1920c0e]  ; -> 01E0283C [f32 1]
004E1C2E  movss    xmm2, dword ptr [rip + 0x1b82fd2]  ; -> 02064C08
004E1C36  movss    xmm3, dword ptr [rip + 0x1b82fce]  ; -> 02064C0C
004E1C3E  addss    xmm2, xmm4
004E1C42  movss    xmm10, dword ptr [rip + 0x1b82fa9]  ; -> 02064BF4
004E1C4B  addss    xmm3, xmm4
004E1C4F  movss    xmm15, dword ptr [rip + 0x1809f18]  ; -> 01CEBB70 [f32 0.5]
004E1C58  cvttps2dq xmm11, xmm0
004E1C5D  shl      eax, 4
004E1C60  movsxd   rcx, eax
004E1C63  lea      eax, [rdx + 0x100]
004E1C69  shl      eax, 4
004E1C6C  cvttps2dq xmm12, xmm1
004E1C71  movups   xmm8, xmmword ptr [rcx + r12]
004E1C76  movsxd   rcx, eax
004E1C79  lea      eax, [rdx + 0x180]
004E1C7F  movups   xmm1, xmmword ptr [rip + 0x1b8300a]  ; -> 02064C90
004E1C86  shl      eax, 4
004E1C89  movups   xmmword ptr [rip + 0x1b8301f], xmm8  ; -> 02064CB0
004E1C91  movups   xmm0, xmmword ptr [rcx + r12]
004E1C96  movsxd   rcx, eax
004E1C99  cvttps2dq xmm13, xmm1
004E1C9E  movss    xmm1, dword ptr [rip + 0x1b82f5e]  ; -> 02064C04
004E1CA6  movups   xmm7, xmmword ptr [rcx + r12]
004E1CAB  movups   xmmword ptr [rip + 0x1b8300e], xmm0  ; -> 02064CC0
004E1CB2  addss    xmm1, xmm4
004E1CB6  shufps   xmm8, xmm8, 0xff
004E1CBB  addss    xmm4, dword ptr [rip + 0x1b82f11]  ; -> 02064BD4
004E1CC3  movaps   xmm0, xmm10
004E1CC7  movss    dword ptr [rip + 0x1b83019], xmm5  ; -> 02064CE8
004E1CCF  mulss    xmm0, dword ptr [rip + 0x1b82ef9]  ; -> 02064BD0
004E1CD7  movaps   xmm6, xmm8
004E1CDB  movss    dword ptr [rip + 0x1b83001], xmm1  ; -> 02064CE4
004E1CE3  mulss    xmm1, xmm8
004E1CE8  addss    xmm4, xmm0
004E1CEC  movss    dword ptr [rip + 0x1b8301c], xmm0  ; -> 02064D10
004E1CF4  movups   xmmword ptr [rip + 0x1b82fd5], xmm7  ; -> 02064CD0
004E1CFB  shufps   xmm7, xmm7, 0xff
004E1CFF  movss    dword ptr [rip + 0x1b82f0d], xmm1  ; -> 02064C14
004E1D07  addss    xmm6, xmm7
004E1D0B  movss    dword ptr [rip + 0x1b83001], xmm4  ; -> 02064D14
004E1D13  addss    xmm4, dword ptr [rip + 0x1920b15]  ; -> 01E02830 [u32 0x00000000]
004E1D1B  movss    dword ptr [rip + 0x1b82fd1], xmm2  ; -> 02064CF4
004E1D23  movss    dword ptr [rip + 0x1b82fcd], xmm5  ; -> 02064CF8
004E1D2B  mulss    xmm6, xmm15
004E1D30  movaps   xmm0, xmm4
004E1D33  movss    dword ptr [rip + 0x1b82fc9], xmm3  ; -> 02064D04
004E1D3B  mulss    xmm0, xmm8
004E1D40  movaps   xmm1, xmm4
004E1D43  movss    dword ptr [rip + 0x1b82fbd], xmm5  ; -> 02064D08
004E1D4B  movss    dword ptr [rip + 0x1b82f8d], xmm4  ; -> 02064CE0
004E1D53  movss    dword ptr [rip + 0x1b82eb5], xmm0  ; -> 02064C10
004E1D5B  movaps   xmm0, xmm5
004E1D5E  mulss    xmm0, xmm8
004E1D63  movss    dword ptr [rip + 0x1b82f85], xmm4  ; -> 02064CF0
004E1D6B  movss    dword ptr [rip + 0x1b82f8d], xmm4  ; -> 02064D00
004E1D73  movss    dword ptr [rip + 0x1b82e9d], xmm0  ; -> 02064C18
004E1D7B  movaps   xmm0, xmm5
004E1D7E  mulss    xmm0, xmm6
004E1D82  mulss    xmm1, xmm6
004E1D86  mulss    xmm2, xmm6
004E1D8A  mulss    xmm4, xmm7
004E1D8E  mulss    xmm3, xmm7
004E1D92  mulss    xmm5, xmm7
004E1D96  movss    dword ptr [rip + 0x1b82e8a], xmm0  ; -> 02064C28
004E1D9E  movss    dword ptr [rip + 0x1b82f26], xmm6  ; -> 02064CCC
004E1DA6  movss    dword ptr [rip + 0x1b82e72], xmm1  ; -> 02064C20
004E1DAE  movss    dword ptr [rip + 0x1b82e6e], xmm2  ; -> 02064C24
004E1DB6  movss    dword ptr [rip + 0x1b82e72], xmm4  ; -> 02064C30
004E1DBE  movss    dword ptr [rip + 0x1b82e6e], xmm3  ; -> 02064C34
004E1DC6  movss    dword ptr [rip + 0x1b82e6a], xmm5  ; -> 02064C38
004E1DCE  movups   xmmword ptr [rip + 0x1b82e9a], xmm11  ; -> 02064C70
004E1DD6  movups   xmmword ptr [rip + 0x1b82ea2], xmm12  ; -> 02064C80
004E1DDE  movups   xmmword ptr [rip + 0x1b82eaa], xmm13  ; -> 02064C90
004E1DE6  movsx    r9d, word ptr [rip + 0x1b82d1e]  ; -> 02064B0C
004E1DEE  movzx    ebx, word ptr [rip + 0x1b82fbf]  ; -> 02064DB4
004E1DF5  lea      eax, [r9 + 4]
004E1DF9  shl      eax, 4
004E1DFC  cdqe     
004E1DFE  movzx    ecx, word ptr [rax + r12]
004E1E03  inc      cx
004E1E06  nop      word ptr [rax + rax]
004E1E10  movss    xmm1, dword ptr [rip + 0x1b82e3c]  ; -> 02064C54
004E1E18  dec      cx
004E1E1B  addss    xmm1, dword ptr [rip + 0x1b82e2d]  ; -> 02064C50
004E1E23  addss    xmm10, dword ptr [rip + 0x1b82dc4]  ; -> 02064BF0
004E1E2C  movss    xmm0, dword ptr [rip + 0x1b82da4]  ; -> 02064BD8
004E1E34  mov      word ptr [rip + 0x1b82f99], cx  ; -> 02064DD4
004E1E3B  ucomiss  xmm0, xmm1
004E1E3E  movss    dword ptr [rip + 0x1b82e0e], xmm1  ; -> 02064C54
004E1E46  movss    dword ptr [rip + 0x1b82da5], xmm10  ; -> 02064BF4
004E1E4F  jp       0x4e1e5a  ; -> 004E1E5A
004E1E51  jne      0x4e1e5a  ; -> 004E1E5A
004E1E53  mov      eax, 1
004E1E58  jmp      0x4e1e5c  ; -> 004E1E5C
004E1E5A  xor      eax, eax
004E1E5C  xor      r8d, r8d
004E1E5F  movsx    edx, bx
004E1E62  comiss   xmm1, xmm0
004E1E65  seta     r8b
004E1E69  shl      r8w, 4
004E1E6E  add      r8w, ax
004E1E72  lea      eax, [rdx + 1]
004E1E75  shl      eax, 4
004E1E78  add      r8w, r8w
004E1E7C  movsxd   rcx, eax
004E1E7F  lea      eax, [rdx + 7]
004E1E82  shl      eax, 4
004E1E85  mov      word ptr [rip + 0x1b82c83], r8w  ; -> 02064B10
004E1E8D  movups   xmmword ptr [rcx + r12], xmm11
004E1E92  movsxd   rcx, eax
004E1E95  lea      eax, [rdx + 0xd]
004E1E98  shl      eax, 4
004E1E9B  movups   xmmword ptr [rcx + r12], xmm12
004E1EA0  movsxd   rcx, eax
004E1EA3  lea      eax, [r9 + 0x20]
004E1EA7  and      ax, r8w
004E1EAB  mov      word ptr [rip + 0x1b82f32], ax  ; -> 02064DE4
004E1EB2  movups   xmmword ptr [rcx + r12], xmm13
004E1EB7  cmp      ax, r9w
004E1EBB  jne      0x4e216a  ; -> 004E216A
004E1EC1  movss    xmm0, dword ptr [rip + 0x1b82d1b]  ; -> 02064BE4
004E1EC9  mulss    xmm0, xmm1
004E1ECD  movss    xmm1, dword ptr [rip + 0x1b82c8b]  ; -> 02064B60
004E1ED5  subss    xmm1, dword ptr [rip + 0x1b82c53]  ; -> 02064B30
004E1EDD  movss    dword ptr [rip + 0x1b82d5f], xmm0  ; -> 02064C44
004E1EE5  movss    xmm0, dword ptr [rip + 0x1b82c77]  ; -> 02064B64
004E1EED  subss    xmm0, dword ptr [rip + 0x1b82c3f]  ; -> 02064B34
004E1EF5  movss    dword ptr [rip + 0x1b82d73], xmm1  ; -> 02064C70
004E1EFD  movss    xmm1, dword ptr [rip + 0x1b82c63]  ; -> 02064B68
004E1F05  subss    xmm1, dword ptr [rip + 0x1b82c2b]  ; -> 02064B38
004E1F0D  movss    dword ptr [rip + 0x1b82d5f], xmm0  ; -> 02064C74
004E1F15  movss    xmm0, dword ptr [rip + 0x1b82c4f]  ; -> 02064B6C
004E1F1D  subss    xmm0, dword ptr [rip + 0x1b82c17]  ; -> 02064B3C
004E1F25  movss    dword ptr [rip + 0x1b82d4b], xmm1  ; -> 02064C78
004E1F2D  movss    dword ptr [rip + 0x1b82d47], xmm0  ; -> 02064C7C
004E1F35  call     0x22cc20  ; -> 0022CC20 fn
004E1F3A  movups   xmm0, xmmword ptr [rip + 0x1b82d6f]  ; -> 02064CB0
004E1F41  movsx    eax, word ptr [rip + 0x1b82e6c]  ; -> 02064DB4
004E1F48  movss    xmm1, dword ptr [rip + 0x1b82c20]  ; -> 02064B70
004E1F50  add      eax, 2
004E1F53  subss    xmm1, dword ptr [rip + 0x1b82be5]  ; -> 02064B40
004E1F5B  shl      eax, 4
004E1F5E  movsxd   rcx, eax
004E1F61  movss    dword ptr [rip + 0x1b82d17], xmm1  ; -> 02064C80
004E1F69  movss    xmm1, dword ptr [rip + 0x1b82c07]  ; -> 02064B78
004E1F71  subss    xmm1, dword ptr [rip + 0x1b82bcf]  ; -> 02064B48
004E1F79  movups   xmmword ptr [rcx + r12], xmm0
004E1F7E  movss    xmm0, dword ptr [rip + 0x1b82bee]  ; -> 02064B74
004E1F86  subss    xmm0, dword ptr [rip + 0x1b82bb6]  ; -> 02064B44
004E1F8E  movss    dword ptr [rip + 0x1b82cf2], xmm1  ; -> 02064C88
004E1F96  movss    dword ptr [rip + 0x1b82ce6], xmm0  ; -> 02064C84
004E1F9E  movss    xmm0, dword ptr [rip + 0x1b82bd6]  ; -> 02064B7C
004E1FA6  subss    xmm0, dword ptr [rip + 0x1b82b9e]  ; -> 02064B4C
004E1FAE  movss    dword ptr [rip + 0x1b82cd6], xmm0  ; -> 02064C8C
004E1FB6  call     0x22cc20  ; -> 0022CC20 fn
004E1FBB  movups   xmm0, xmmword ptr [rip + 0x1b82cfe]  ; -> 02064CC0
004E1FC2  movsx    eax, word ptr [rip + 0x1b82deb]  ; -> 02064DB4
004E1FC9  movss    xmm1, dword ptr [rip + 0x1b82baf]  ; -> 02064B80
004E1FD1  add      eax, 8
004E1FD4  subss    xmm1, dword ptr [rip + 0x1b82b74]  ; -> 02064B50
004E1FDC  shl      eax, 4
004E1FDF  movsxd   rcx, eax
004E1FE2  movss    dword ptr [rip + 0x1b82ca6], xmm1  ; -> 02064C90
004E1FEA  movss    xmm1, dword ptr [rip + 0x1b82b96]  ; -> 02064B88
004E1FF2  subss    xmm1, dword ptr [rip + 0x1b82b5e]  ; -> 02064B58
004E1FFA  movups   xmmword ptr [rcx + r12], xmm0
004E1FFF  movss    xmm0, dword ptr [rip + 0x1b82b7d]  ; -> 02064B84
004E2007  subss    xmm0, dword ptr [rip + 0x1b82b45]  ; -> 02064B54
004E200F  movss    dword ptr [rip + 0x1b82c81], xmm1  ; -> 02064C98
004E2017  movss    dword ptr [rip + 0x1b82c75], xmm0  ; -> 02064C94
004E201F  movss    xmm0, dword ptr [rip + 0x1b82b65]  ; -> 02064B8C
004E2027  subss    xmm0, dword ptr [rip + 0x1b82b2d]  ; -> 02064B5C
004E202F  movss    dword ptr [rip + 0x1b82c65], xmm0  ; -> 02064C9C
004E2037  call     0x22cc20  ; -> 0022CC20 fn
004E203C  movss    xmm1, dword ptr [rip + 0x1b82c00]  ; -> 02064C44
004E2044  movsx    ebx, word ptr [rip + 0x1b82d69]  ; -> 02064DB4
004E204B  movups   xmm0, xmmword ptr [rip + 0x1b82c7e]  ; -> 02064CD0
004E2052  mov      r11d, ebx
004E2055  movss    xmm3, dword ptr [rip + 0x1b82c17]  ; -> 02064C74
004E205D  movss    xmm2, dword ptr [rip + 0x1b82c0b]  ; -> 02064C70
004E2065  lea      eax, [rbx + 0xe]
004E2068  movss    xmm4, dword ptr [rip + 0x1b82c08]  ; -> 02064C78
004E2070  movss    xmm5, dword ptr [rip + 0x1b82c04]  ; -> 02064C7C
004E2078  movss    xmm7, dword ptr [rip + 0x1b82c04]  ; -> 02064C84
004E2080  movss    xmm6, dword ptr [rip + 0x1b82bf8]  ; -> 02064C80
004E2088  movss    xmm8, dword ptr [rip + 0x1b82bf7]  ; -> 02064C88
004E2091  movss    xmm10, dword ptr [rip + 0x1b82bf2]  ; -> 02064C8C
004E209A  movss    xmm12, dword ptr [rip + 0x1b82bf1]  ; -> 02064C94
004E20A3  movss    xmm11, dword ptr [rip + 0x1b82be4]  ; -> 02064C90
004E20AC  shl      eax, 4
004E20AF  movsxd   rdx, eax
004E20B2  mulss    xmm3, xmm1
004E20B6  mulss    xmm2, xmm1
004E20BA  movups   xmmword ptr [rdx + r12], xmm0
004E20BF  mulss    xmm4, xmm1
004E20C3  mulss    xmm5, xmm1
004E20C7  mulss    xmm7, xmm1
004E20CB  mulss    xmm6, xmm1
004E20CF  mulss    xmm8, xmm1
004E20D4  mulss    xmm10, xmm1
004E20D9  mulss    xmm12, xmm1
004E20DE  movss    xmm13, dword ptr [rip + 0x1b82bb1]  ; -> 02064C98
004E20E7  movss    xmm14, dword ptr [rip + 0x1b82bac]  ; -> 02064C9C
004E20F0  addss    xmm2, dword ptr [rip + 0x1b82a38]  ; -> 02064B30
004E20F8  addss    xmm3, dword ptr [rip + 0x1b82a34]  ; -> 02064B34
004E2100  addss    xmm4, dword ptr [rip + 0x1b82a30]  ; -> 02064B38
004E2108  addss    xmm5, dword ptr [rip + 0x1b82a2c]  ; -> 02064B3C
004E2110  addss    xmm6, dword ptr [rip + 0x1b82a28]  ; -> 02064B40
004E2118  addss    xmm7, dword ptr [rip + 0x1b82a24]  ; -> 02064B44
004E2120  addss    xmm8, dword ptr [rip + 0x1b82a1f]  ; -> 02064B48
004E2129  addss    xmm10, dword ptr [rip + 0x1b82a1a]  ; -> 02064B4C
004E2132  addss    xmm12, dword ptr [rip + 0x1b82a19]  ; -> 02064B54
004E213B  mulss    xmm13, xmm1
004E2140  mulss    xmm14, xmm1
004E2145  addss    xmm13, dword ptr [rip + 0x1b82a0a]  ; -> 02064B58
004E214E  mulss    xmm11, xmm1
004E2153  addss    xmm14, dword ptr [rip + 0x1b82a00]  ; -> 02064B5C
004E215C  addss    xmm11, dword ptr [rip + 0x1b829eb]  ; -> 02064B50
004E2165  jmp      0x4e2412  ; -> 004E2412
004E216A  subss    xmm1, dword ptr [rip + 0x1b82a6e]  ; -> 02064BE0
004E2172  movss    xmm0, dword ptr [rip + 0x1b82a16]  ; -> 02064B90
004E217A  subss    xmm0, dword ptr [rip + 0x1b829de]  ; -> 02064B60
004E2182  mulss    xmm1, dword ptr [rip + 0x1b82a62]  ; -> 02064BEC
004E218A  movss    dword ptr [rip + 0x1b82ade], xmm0  ; -> 02064C70
004E2192  movss    xmm0, dword ptr [rip + 0x1b829fe]  ; -> 02064B98
004E219A  subss    xmm0, dword ptr [rip + 0x1b829c6]  ; -> 02064B68
004E21A2  movss    dword ptr [rip + 0x1b82a9a], xmm1  ; -> 02064C44
004E21AA  movss    xmm1, dword ptr [rip + 0x1b829e2]  ; -> 02064B94
004E21B2  subss    xmm1, dword ptr [rip + 0x1b829aa]  ; -> 02064B64
004E21BA  movss    dword ptr [rip + 0x1b82ab6], xmm0  ; -> 02064C78
004E21C2  movss    dword ptr [rip + 0x1b82aaa], xmm1  ; -> 02064C74
004E21CA  movss    xmm1, dword ptr [rip + 0x1b829ca]  ; -> 02064B9C
004E21D2  subss    xmm1, dword ptr [rip + 0x1b82992]  ; -> 02064B6C
004E21DA  movss    dword ptr [rip + 0x1b82a9a], xmm1  ; -> 02064C7C
004E21E2  call     0x22cc20  ; -> 0022CC20 fn
004E21E7  movups   xmm0, xmmword ptr [rip + 0x1b82ac2]  ; -> 02064CB0
004E21EE  movsx    eax, word ptr [rip + 0x1b82bbf]  ; -> 02064DB4
004E21F5  movss    xmm1, dword ptr [rip + 0x1b829a3]  ; -> 02064BA0
004E21FD  add      eax, 2
004E2200  subss    xmm1, dword ptr [rip + 0x1b82968]  ; -> 02064B70
004E2208  shl      eax, 4
004E220B  movsxd   rcx, eax
004E220E  movss    dword ptr [rip + 0x1b82a6a], xmm1  ; -> 02064C80
004E2216  movss    xmm1, dword ptr [rip + 0x1b8298a]  ; -> 02064BA8
004E221E  subss    xmm1, dword ptr [rip + 0x1b82952]  ; -> 02064B78
004E2226  movups   xmmword ptr [rcx + r12], xmm0
004E222B  movss    xmm0, dword ptr [rip + 0x1b82971]  ; -> 02064BA4
004E2233  subss    xmm0, dword ptr [rip + 0x1b82939]  ; -> 02064B74
004E223B  movss    dword ptr [rip + 0x1b82a45], xmm1  ; -> 02064C88
004E2243  movss    dword ptr [rip + 0x1b82a39], xmm0  ; -> 02064C84
004E224B  movss    xmm0, dword ptr [rip + 0x1b82959]  ; -> 02064BAC
004E2253  subss    xmm0, dword ptr [rip + 0x1b82921]  ; -> 02064B7C
004E225B  movss    dword ptr [rip + 0x1b82a29], xmm0  ; -> 02064C8C
004E2263  call     0x22cc20  ; -> 0022CC20 fn
004E2268  movups   xmm0, xmmword ptr [rip + 0x1b82a51]  ; -> 02064CC0
004E226F  movsx    eax, word ptr [rip + 0x1b82b3e]  ; -> 02064DB4
004E2276  movss    xmm1, dword ptr [rip + 0x1b82932]  ; -> 02064BB0
004E227E  add      eax, 8
004E2281  subss    xmm1, dword ptr [rip + 0x1b828f7]  ; -> 02064B80
004E2289  shl      eax, 4
004E228C  movsxd   rcx, eax
004E228F  movss    dword ptr [rip + 0x1b829f9], xmm1  ; -> 02064C90
004E2297  movss    xmm1, dword ptr [rip + 0x1b82919]  ; -> 02064BB8
004E229F  subss    xmm1, dword ptr [rip + 0x1b828e1]  ; -> 02064B88
004E22A7  movups   xmmword ptr [rcx + r12], xmm0
004E22AC  movss    xmm0, dword ptr [rip + 0x1b82900]  ; -> 02064BB4
004E22B4  subss    xmm0, dword ptr [rip + 0x1b828c8]  ; -> 02064B84
004E22BC  movss    dword ptr [rip + 0x1b829d4], xmm1  ; -> 02064C98
004E22C4  movss    dword ptr [rip + 0x1b829c8], xmm0  ; -> 02064C94
004E22CC  movss    xmm0, dword ptr [rip + 0x1b828e8]  ; -> 02064BBC
004E22D4  subss    xmm0, dword ptr [rip + 0x1b828b0]  ; -> 02064B8C
004E22DC  movss    dword ptr [rip + 0x1b829b8], xmm0  ; -> 02064C9C
004E22E4  call     0x22cc20  ; -> 0022CC20 fn
004E22E9  movss    xmm1, dword ptr [rip + 0x1b82953]  ; -> 02064C44
004E22F1  movsx    ebx, word ptr [rip + 0x1b82abc]  ; -> 02064DB4
004E22F8  movups   xmm0, xmmword ptr [rip + 0x1b829d1]  ; -> 02064CD0
004E22FF  mov      r11d, ebx
004E2302  movss    xmm3, dword ptr [rip + 0x1b8296a]  ; -> 02064C74
004E230A  movss    xmm2, dword ptr [rip + 0x1b8295e]  ; -> 02064C70
004E2312  lea      eax, [rbx + 0xe]
004E2315  movss    xmm4, dword ptr [rip + 0x1b8295b]  ; -> 02064C78
004E231D  movss    xmm5, dword ptr [rip + 0x1b82957]  ; -> 02064C7C
004E2325  movss    xmm7, dword ptr [rip + 0x1b82957]  ; -> 02064C84
004E232D  movss    xmm6, dword ptr [rip + 0x1b8294b]  ; -> 02064C80
004E2335  movss    xmm8, dword ptr [rip + 0x1b8294a]  ; -> 02064C88
004E233E  movss    xmm10, dword ptr [rip + 0x1b82945]  ; -> 02064C8C
004E2347  movss    xmm12, dword ptr [rip + 0x1b82944]  ; -> 02064C94
004E2350  movss    xmm11, dword ptr [rip + 0x1b82937]  ; -> 02064C90
004E2359  shl      eax, 4
004E235C  movsxd   rdx, eax
004E235F  mulss    xmm3, xmm1
004E2363  mulss    xmm2, xmm1
004E2367  movups   xmmword ptr [rdx + r12], xmm0
004E236C  mulss    xmm4, xmm1
004E2370  mulss    xmm5, xmm1
004E2374  mulss    xmm7, xmm1
004E2378  mulss    xmm6, xmm1
004E237C  mulss    xmm8, xmm1
004E2381  mulss    xmm10, xmm1
004E2386  mulss    xmm12, xmm1
004E238B  movss    xmm13, dword ptr [rip + 0x1b82904]  ; -> 02064C98
004E2394  movss    xmm14, dword ptr [rip + 0x1b828ff]  ; -> 02064C9C
004E239D  addss    xmm2, dword ptr [rip + 0x1b827bb]  ; -> 02064B60
004E23A5  addss    xmm3, dword ptr [rip + 0x1b827b7]  ; -> 02064B64
004E23AD  addss    xmm4, dword ptr [rip + 0x1b827b3]  ; -> 02064B68
004E23B5  addss    xmm5, dword ptr [rip + 0x1b827af]  ; -> 02064B6C
004E23BD  addss    xmm6, dword ptr [rip + 0x1b827ab]  ; -> 02064B70
004E23C5  addss    xmm7, dword ptr [rip + 0x1b827a7]  ; -> 02064B74
004E23CD  addss    xmm8, dword ptr [rip + 0x1b827a2]  ; -> 02064B78
004E23D6  addss    xmm10, dword ptr [rip + 0x1b8279d]  ; -> 02064B7C
004E23DF  addss    xmm12, dword ptr [rip + 0x1b8279c]  ; -> 02064B84
004E23E8  mulss    xmm13, xmm1
004E23ED  mulss    xmm14, xmm1
004E23F2  addss    xmm13, dword ptr [rip + 0x1b8278d]  ; -> 02064B88
004E23FB  mulss    xmm11, xmm1
004E2400  addss    xmm14, dword ptr [rip + 0x1b82783]  ; -> 02064B8C
004E2409  addss    xmm11, dword ptr [rip + 0x1b8276e]  ; -> 02064B80
004E2412  movups   xmm0, xmmword ptr [rip + 0x1b827f7]  ; -> 02064C10
004E2419  movzx    r8d, word ptr [rip + 0x1b829ab]  ; -> 02064DCC
004E2421  mov      eax, ebx
004E2423  movzx    r9d, word ptr [rip + 0x1b8299d]  ; -> 02064DC8
004E242B  shl      eax, 4
004E242E  movsxd   rcx, eax
004E2431  lea      eax, [rbx + 6]
004E2434  shl      eax, 4
004E2437  movss    dword ptr [rip + 0x1b82839], xmm4  ; -> 02064C78
004E243F  movss    dword ptr [rip + 0x1b8282d], xmm3  ; -> 02064C74
004E2447  movups   xmmword ptr [rcx + r12], xmm0
004E244C  movsxd   rcx, eax
004E244F  lea      eax, [rbx + 0xc]
004E2452  movups   xmm0, xmmword ptr [rip + 0x1b827c7]  ; -> 02064C20
004E2459  shl      eax, 4
004E245C  movss    dword ptr [rip + 0x1b8280c], xmm2  ; -> 02064C70
004E2464  movups   xmmword ptr [rcx + r12], xmm0
004E2469  movsxd   rcx, eax
004E246C  lea      eax, [rbx + 2]
004E246F  movups   xmm0, xmmword ptr [rip + 0x1b827ba]  ; -> 02064C30
004E2476  shl      eax, 4
004E2479  movss    dword ptr [rip + 0x1b8281a], xmm14  ; -> 02064C9C
004E2482  movups   xmmword ptr [rcx + r12], xmm0
004E2487  movsxd   rcx, eax
004E248A  lea      eax, [rbx + 8]
004E248D  shl      eax, 4
004E2490  comiss   xmm9, xmm2
004E2494  mov      dword ptr [rcx + r12 + 0xc], r9d
004E2499  movsxd   rcx, eax
004E249C  mov      dword ptr [rcx + r12 + 0xc], r8d
004E24A1  mov      dword ptr [rdx + r12 + 0xc], r8d
004E24A6  movss    dword ptr [rip + 0x1b827e9], xmm13  ; -> 02064C98
004E24AF  movss    dword ptr [rip + 0x1b827dc], xmm12  ; -> 02064C94
004E24B8  movss    dword ptr [rip + 0x1b827cf], xmm11  ; -> 02064C90
004E24C1  movss    dword ptr [rip + 0x1b827c2], xmm10  ; -> 02064C8C
004E24CA  movss    dword ptr [rip + 0x1b827b5], xmm8  ; -> 02064C88
004E24D3  movss    dword ptr [rip + 0x1b827a9], xmm7  ; -> 02064C84
004E24DB  movss    dword ptr [rip + 0x1b8279d], xmm6  ; -> 02064C80
004E24E3  movss    dword ptr [rip + 0x1b82791], xmm5  ; -> 02064C7C
004E24EB  ja       0x4e24f7  ; -> 004E24F7
004E24ED  mov      dword ptr [rip + 0x1b82779], 0x437f0000  ; -> 02064C70
004E24F7  comiss   xmm9, xmm3
004E24FB  ja       0x4e2507  ; -> 004E2507
004E24FD  mov      dword ptr [rip + 0x1b8276d], 0x437f0000  ; -> 02064C74
004E2507  comiss   xmm9, xmm4
004E250B  ja       0x4e2517  ; -> 004E2517
004E250D  mov      dword ptr [rip + 0x1b82761], 0x437f0000  ; -> 02064C78
004E2517  comiss   xmm9, xmm5
004E251B  ja       0x4e2527  ; -> 004E2527
004E251D  mov      dword ptr [rip + 0x1b82755], 0x437f0000  ; -> 02064C7C
004E2527  lea      eax, [r11 + 5]
004E252B  shl      eax, 4
004E252E  comiss   xmm9, xmm6
004E2532  movsxd   rbp, eax
004E2535  mov      dword ptr [r12 + rbp + 0xc], r9d
004E253A  ja       0x4e2546  ; -> 004E2546
004E253C  mov      dword ptr [rip + 0x1b8273a], 0x437f0000  ; -> 02064C80
004E2546  comiss   xmm9, xmm7
004E254A  ja       0x4e2556  ; -> 004E2556
004E254C  mov      dword ptr [rip + 0x1b8272e], 0x437f0000  ; -> 02064C84
004E2556  comiss   xmm9, xmm8
004E255A  ja       0x4e2566  ; -> 004E2566
004E255C  mov      dword ptr [rip + 0x1b82722], 0x437f0000  ; -> 02064C88
004E2566  comiss   xmm9, xmm10
004E256A  ja       0x4e2576  ; -> 004E2576
004E256C  mov      dword ptr [rip + 0x1b82716], 0x437f0000  ; -> 02064C8C
004E2576  lea      eax, [r11 + 0xb]
004E257A  shl      eax, 4
004E257D  comiss   xmm9, xmm11
004E2581  movsxd   rsi, eax
004E2584  mov      dword ptr [rsi + r12 + 0xc], r8d
004E2589  ja       0x4e2595  ; -> 004E2595
004E258B  mov      dword ptr [rip + 0x1b826fb], 0x437f0000  ; -> 02064C90
004E2595  comiss   xmm9, xmm12
004E2599  ja       0x4e25a5  ; -> 004E25A5
004E259B  mov      dword ptr [rip + 0x1b826ef], 0x437f0000  ; -> 02064C94
004E25A5  comiss   xmm9, xmm13
004E25A9  ja       0x4e25b5  ; -> 004E25B5
004E25AB  mov      dword ptr [rip + 0x1b826e3], 0x437f0000  ; -> 02064C98
004E25B5  comiss   xmm9, xmm14
004E25B9  ja       0x4e25c5  ; -> 004E25C5
004E25BB  mov      dword ptr [rip + 0x1b826d7], 0x437f0000  ; -> 02064C9C
004E25C5  lea      eax, [r11 + 0x11]
004E25C9  shl      eax, 4
004E25CC  movsxd   rdi, eax
004E25CF  nop      
004E25D0  mov      dword ptr [rdi + r12 + 0xc], r8d
004E25D5  movzx    eax, word ptr [rip + 0x1b827e0]  ; -> 02064DBC
004E25DC  movups   xmm0, xmmword ptr [rip + 0x1b8268d]  ; -> 02064C70
004E25E3  inc      ax
004E25E6  mov      dword ptr [rip + 0x1b82514], 0x3f000000  ; -> 02064B04
004E25F0  movss    xmm4, dword ptr [rip + 0x192023c]  ; -> 01E02834 [u32 0x00000000]
004E25F8  addss    xmm4, dword ptr [rip + 0x1b825d4]  ; -> 02064BD4
004E2600  movss    xmm10, dword ptr [rip + 0x1b825eb]  ; -> 02064BF4
004E2609  movsx    r8d, ax
004E260D  movaps   xmm1, xmm10
004E2611  mulss    xmm1, dword ptr [rip + 0x1b825b7]  ; -> 02064BD0
004E2619  mov      word ptr [rip + 0x1b8279c], ax  ; -> 02064DBC
004E2620  cvttps2dq xmm11, xmm0
004E2625  lea      eax, [r8 + 0xff]
004E262C  shl      eax, 4
004E262F  movsxd   rcx, eax
004E2632  lea      eax, [r8 + 0x100]
004E2639  shl      eax, 4
004E263C  movups   xmm0, xmmword ptr [rip + 0x1b8263d]  ; -> 02064C80
004E2643  movsxd   rdx, eax
004E2646  lea      eax, [r8 + 0x80]
004E264D  movzx    r10d, word ptr [rcx + r12 + 0xc]
004E2653  addss    xmm4, xmm1
004E2657  shl      eax, 4
004E265A  movsxd   rcx, eax
004E265D  lea      eax, [r8 + 0x180]
004E2664  movsx    r9d, word ptr [rdx + r12 + 0xc]
004E266A  shl      eax, 4
004E266D  or       r10w, r9w
004E2671  cvttps2dq xmm12, xmm0
004E2676  mov      word ptr [rip + 0x1b82746], r9w  ; -> 02064DC4
004E267E  mov      word ptr [rip + 0x1b8273a], r10w  ; -> 02064DC0
004E2686  movups   xmm2, xmmword ptr [rcx + r12]
004E268B  movsxd   rcx, eax
004E268E  lea      eax, [r11 + 4]
004E2692  movups   xmm0, xmmword ptr [rip + 0x1b825f7]  ; -> 02064C90
004E2699  shl      eax, 4
004E269C  movaps   xmm5, xmm2
004E269F  movss    dword ptr [rip + 0x1b8266d], xmm4  ; -> 02064D14
004E26A7  movups   xmm3, xmmword ptr [rcx + r12]
004E26AC  movsxd   rcx, eax
004E26AF  lea      eax, [r11 + 0xa]
004E26B3  addss    xmm4, dword ptr [rip + 0x1920175]  ; -> 01E02830 [u32 0x00000000]
004E26BB  cvttps2dq xmm13, xmm0
004E26C0  shl      eax, 4
004E26C3  movups   xmm0, xmmword ptr [rdx + r12]
004E26C8  movups   xmmword ptr [rcx + r12], xmm11
004E26CD  movsxd   rcx, eax
004E26D0  lea      eax, [r11 + 0x10]
004E26D4  shufps   xmm5, xmm2, 0xff
004E26D8  movaps   xmm7, xmm3
004E26DB  movups   xmmword ptr [rip + 0x1b825de], xmm0  ; -> 02064CC0
004E26E2  shl      eax, 4
004E26E5  movsd    xmm0, qword ptr [rip + 0x1b825d3]  ; -> 02064CC0
004E26ED  movaps   xmm6, xmm5
004E26F0  movups   xmmword ptr [rcx + r12], xmm12
004E26F5  movsxd   rcx, eax
004E26F8  mov      eax, dword ptr [rip + 0x1b825ca]  ; -> 02064CC8
004E26FE  shufps   xmm7, xmm3, 0xff
004E2702  addss    xmm6, xmm7
004E2706  movss    dword ptr [rip + 0x1b82602], xmm1  ; -> 02064D10
004E270E  movups   xmmword ptr [rcx + r12], xmm13
004E2713  movsd    qword ptr [r12 + rbp], xmm2
004E2719  movups   xmmword ptr [rip + 0x1b82590], xmm2  ; -> 02064CB0
004E2720  psrldq   xmm2, 8
004E2725  movd     dword ptr [r12 + rbp + 8], xmm2
004E272C  movsd    qword ptr [rsi + r12], xmm0
004E2732  movaps   xmm0, xmm4
004E2735  mov      dword ptr [rsi + r12 + 8], eax
004E273A  movsd    qword ptr [rdi + r12], xmm3
004E2740  mulss    xmm6, xmm15
004E2745  movups   xmmword ptr [rip + 0x1b82584], xmm3  ; -> 02064CD0
004E274C  psrldq   xmm3, 8
004E2751  movd     dword ptr [rdi + r12 + 8], xmm3
004E2758  movss    dword ptr [rip + 0x1b8256c], xmm6  ; -> 02064CCC
004E2760  movss    dword ptr [rip + 0x1b82578], xmm4  ; -> 02064CE0
004E2768  movss    dword ptr [rip + 0x1b82580], xmm4  ; -> 02064CF0
004E2770  movss    dword ptr [rip + 0x1b82588], xmm4  ; -> 02064D00
004E2778  movups   xmmword ptr [rip + 0x1b824f0], xmm11  ; -> 02064C70
004E2780  movups   xmmword ptr [rip + 0x1b824f8], xmm12  ; -> 02064C80
004E2788  movups   xmmword ptr [rip + 0x1b82500], xmm13  ; -> 02064C90
004E2790  mulss    xmm0, xmm5
004E2794  movss    xmm1, dword ptr [rip + 0x1b82548]  ; -> 02064CE4
004E279C  movzx    r9d, word ptr [rip + 0x1b82368]  ; -> 02064B0C
004E27A4  mulss    xmm1, xmm5
004E27A8  movss    dword ptr [rip + 0x1b82460], xmm0  ; -> 02064C10
004E27B0  movss    xmm0, dword ptr [rip + 0x1b82530]  ; -> 02064CE8
004E27B8  movss    dword ptr [rip + 0x1b82454], xmm1  ; -> 02064C14
004E27C0  movaps   xmm1, xmm4
004E27C3  mulss    xmm1, xmm6
004E27C7  mulss    xmm0, xmm5
004E27CB  mulss    xmm4, xmm7
004E27CF  movss    dword ptr [rip + 0x1b82449], xmm1  ; -> 02064C20
004E27D7  movss    xmm1, dword ptr [rip + 0x1b82519]  ; -> 02064CF8
004E27DF  movss    dword ptr [rip + 0x1b82431], xmm0  ; -> 02064C18
004E27E7  movss    xmm0, dword ptr [rip + 0x1b82505]  ; -> 02064CF4
004E27EF  mulss    xmm1, xmm6
004E27F3  mulss    xmm0, xmm6
004E27F7  movss    dword ptr [rip + 0x1b82431], xmm4  ; -> 02064C30
004E27FF  movss    dword ptr [rip + 0x1b82421], xmm1  ; -> 02064C28
004E2807  movss    xmm1, dword ptr [rip + 0x1b824f9]  ; -> 02064D08
004E280F  movss    dword ptr [rip + 0x1b8240d], xmm0  ; -> 02064C24
004E2817  movss    xmm0, dword ptr [rip + 0x1b824e5]  ; -> 02064D04
004E281F  mulss    xmm1, xmm7
004E2823  mulss    xmm0, xmm7
004E2827  movss    dword ptr [rip + 0x1b82409], xmm1  ; -> 02064C38
004E282F  movss    dword ptr [rip + 0x1b823fd], xmm0  ; -> 02064C34
004E2837  cmp      r9w, r10w
004E283B  jne      0x4e28d1  ; -> 004E28D1
004E2841  movups   xmm0, xmmword ptr [rip + 0x1b823c8]  ; -> 02064C10
004E2848  add      word ptr [rip + 0x1b82568], 3  ; -> 02064DB8
004E2850  lea      eax, [r11 + 3]
004E2854  shl      eax, 4
004E2857  add      bx, 0x12
004E285B  movsxd   rcx, eax
004E285E  mov      rdx, r14
004E2861  lea      eax, [r11 + 9]
004E2865  mov      word ptr [rip + 0x1b82548], bx  ; -> 02064DB4
004E286C  shl      eax, 4
004E286F  movups   xmmword ptr [rcx + r12], xmm0
004E2874  movsxd   rcx, eax
004E2877  lea      eax, [r11 + 0xf]
004E287B  movups   xmm0, xmmword ptr [rip + 0x1b8239e]  ; -> 02064C20
004E2882  shl      eax, 4
004E2885  movups   xmmword ptr [rcx + r12], xmm0
004E288A  movsxd   rcx, eax
004E288D  movups   xmm0, xmmword ptr [rip + 0x1b8239c]  ; -> 02064C30
004E2894  movups   xmmword ptr [rcx + r12], xmm0
004E2899  mov      rcx, r15
004E289C  call     0x4df360  ; -> 004DF360 fn
004E28A1  movzx    r9d, word ptr [rip + 0x1b82263]  ; -> 02064B0C
004E28A9  movss    xmm10, dword ptr [rip + 0x1b82342]  ; -> 02064BF4
004E28B2  movzx    ebx, word ptr [rip + 0x1b824fb]  ; -> 02064DB4
004E28B9  movups   xmm11, xmmword ptr [rip + 0x1b823af]  ; -> 02064C70
004E28C1  movups   xmm12, xmmword ptr [rip + 0x1b823b7]  ; -> 02064C80
004E28C9  movups   xmm13, xmmword ptr [rip + 0x1b823bf]  ; -> 02064C90
004E28D1  movzx    ecx, word ptr [rip + 0x1b824fc]  ; -> 02064DD4
004E28D8  test     cx, cx
004E28DB  jg       0x4e1e10  ; -> 004E1E10
004E28E1  movaps   xmm14, xmmword ptr [rsp + 0x50]
004E28E7  lea      r11, [rsp + 0xe0]
004E28EF  movaps   xmm6, xmmword ptr [r11 - 0x10]
004E28F4  movaps   xmm7, xmmword ptr [r11 - 0x20]
004E28F9  movaps   xmm8, xmmword ptr [r11 - 0x30]
004E28FE  movaps   xmm9, xmmword ptr [r11 - 0x40]
004E2903  movaps   xmm10, xmmword ptr [r11 - 0x50]
004E2908  movaps   xmm11, xmmword ptr [r11 - 0x60]
004E290D  movaps   xmm12, xmmword ptr [r11 - 0x70]
004E2912  movaps   xmm13, xmmword ptr [r11 - 0x80]
004E2917  movaps   xmm15, xmmword ptr [rsp + 0x40]
004E291D  mov      rsp, r11
004E2920  pop      r15
004E2922  pop      r14
004E2924  pop      r12
004E2926  pop      rdi
004E2927  pop      rsi
004E2928  pop      rbp
004E2929  pop      rbx
004E292A  ret      
```

## 004ECC50 (3334 B, extent 004ECC50-004ED956)

Page context: "README.md), control 'uq204_emits.py' E4). '00522300' calls '003A3010' at '005227C5', a raw packet that the PC drain never submits. '00526A10' calls '003A34D0' at '00526D2D', a GiVmax running program '004ECC50'. What stands below is that neither reaches a '0054xxxx' terminal.* They make the *same kinds* of calls as the other six — '0026EE00' to compose, '0042FDB0' on the workbench, '00462260', and the authored-expression evaluators '0043"

```
004ECC50  mov      rax, rsp
004ECC53  mov      qword ptr [rax + 8], rbx
004ECC57  mov      qword ptr [rax + 0x10], rsi
004ECC5B  push     rdi
004ECC5C  sub      rsp, 0xd0
004ECC63  movaps   xmmword ptr [rax - 0x18], xmm6
004ECC67  lea      rsi, [rip + 0x1b781c2]  ; -> 02064E30
004ECC6E  movaps   xmmword ptr [rax - 0x28], xmm7
004ECC72  mov      rdi, rcx
004ECC75  movaps   xmmword ptr [rax - 0x38], xmm8
004ECC7A  xor      r8d, r8d
004ECC7D  movaps   xmmword ptr [rax - 0x48], xmm9
004ECC82  mov      rbx, rdx
004ECC85  movaps   xmmword ptr [rax - 0x58], xmm10
004ECC8A  movaps   xmmword ptr [rax - 0x68], xmm11
004ECC8F  movaps   xmmword ptr [rax - 0x78], xmm12
004ECC94  movzx    eax, word ptr [rip + 0x1b77e71]  ; -> 02064B0C
004ECC9B  add      ax, 9
004ECC9F  movaps   xmmword ptr [rsp + 0x50], xmm13
004ECCA5  mov      word ptr [rip + 0x1b78128], ax  ; -> 02064DD4
004ECCAC  cwde     
004ECCAD  shl      eax, 4
004ECCB0  movsxd   rcx, eax
004ECCB3  add      rcx, rsi
004ECCB6  movaps   xmmword ptr [rsp + 0x40], xmm14
004ECCBC  movaps   xmmword ptr [rsp + 0x30], xmm15
004ECCC2  call     rdi
004ECCC4  movsx    edx, word ptr [rip + 0x1b77e41]  ; -> 02064B0C
004ECCCB  mov      ecx, edx
004ECCCD  shl      ecx, 4
004ECCD0  movsxd   rax, ecx
004ECCD3  movups   xmm5, xmmword ptr [rax + rsi]
004ECCD7  lea      eax, [rcx + 0x10]
004ECCDA  movsxd   rcx, eax
004ECCDD  lea      eax, [rdx + 3]
004ECCE0  shl      eax, 4
004ECCE3  movups   xmmword ptr [rip + 0x1b77e46], xmm5  ; -> 02064B30
004ECCEA  movups   xmm4, xmmword ptr [rcx + rsi]
004ECCEE  movsxd   rcx, eax
004ECCF1  lea      eax, [rdx + 4]
004ECCF4  shl      eax, 4
004ECCF7  movups   xmmword ptr [rip + 0x1b77e42], xmm4  ; -> 02064B40
004ECCFE  movups   xmm3, xmmword ptr [rcx + rsi]
004ECD02  movsxd   rcx, eax
004ECD05  lea      eax, [rdx + 5]
004ECD08  shl      eax, 4
004ECD0B  movups   xmmword ptr [rip + 0x1b77e3e], xmm3  ; -> 02064B50
004ECD12  movups   xmm0, xmmword ptr [rcx + rsi]
004ECD16  movsxd   rcx, eax
004ECD19  lea      eax, [rdx + 6]
004ECD1C  shl      eax, 4
004ECD1F  addss    xmm3, xmm5
004ECD23  movups   xmmword ptr [rip + 0x1b77e36], xmm0  ; -> 02064B60
004ECD2A  movups   xmm1, xmmword ptr [rcx + rsi]
004ECD2E  movsxd   rcx, eax
004ECD31  lea      eax, [rdx + 7]
004ECD34  shl      eax, 4
004ECD37  movups   xmmword ptr [rip + 0x1b77e32], xmm1  ; -> 02064B70
004ECD3E  movups   xmm2, xmmword ptr [rcx + rsi]
004ECD42  movsxd   rcx, eax
004ECD45  lea      eax, [rdx + 2]
004ECD48  shufps   xmm1, xmm1, 0xff
004ECD4C  movss    dword ptr [rsp + 0x2c], xmm1
004ECD52  movd     xmm1, dword ptr [rsp + 0x2c]
004ECD58  movups   xmm0, xmmword ptr [rcx + rsi]
004ECD5C  shl      eax, 4
004ECD5F  movups   xmmword ptr [rip + 0x1b77e1a], xmm2  ; -> 02064B80
004ECD66  movsxd   rcx, eax
004ECD69  cvtdq2ps xmm1, xmm1
004ECD6C  movzx    eax, word ptr [rcx + rsi]
004ECD70  mov      word ptr [rip + 0x1b78045], ax  ; -> 02064DBC
004ECD77  shufps   xmm2, xmm2, 0xff
004ECD7B  movss    dword ptr [rsp + 0x2c], xmm2
004ECD81  movaps   xmm2, xmm4
004ECD84  shufps   xmm2, xmm4, 0xff
004ECD88  movups   xmmword ptr [rip + 0x1b77e01], xmm0  ; -> 02064B90
004ECD8F  movaps   xmm0, xmm2
004ECD92  movss    dword ptr [rip + 0x1b77db6], xmm3  ; -> 02064B50
004ECD9A  mulss    xmm0, xmm1
004ECD9E  movd     xmm1, dword ptr [rsp + 0x2c]
004ECDA4  cvtdq2ps xmm1, xmm1
004ECDA7  cvttss2si eax, xmm0
004ECDAB  mulss    xmm1, xmm2
004ECDAF  mov      dword ptr [rip + 0x1b77dc7], eax  ; -> 02064B7C
004ECDB5  cvttss2si eax, xmm1
004ECDB9  mov      dword ptr [rip + 0x1b77dcd], eax  ; -> 02064B8C
004ECDBF  movss    xmm0, dword ptr [rip + 0x1b77d8d]  ; -> 02064B54
004ECDC7  movaps   xmm1, xmm5
004ECDCA  shufps   xmm1, xmm5, 0x55
004ECDCE  xorps    xmm9, xmm9
004ECDD2  subss    xmm5, xmm4
004ECDD6  movss    dword ptr [rip + 0x1b77d62], xmm4  ; -> 02064B40
004ECDDE  shufps   xmm4, xmm4, 0x55
004ECDE2  addss    xmm0, xmm1
004ECDE6  subss    xmm1, xmm4
004ECDEA  movss    dword ptr [rip + 0x1b77d52], xmm4  ; -> 02064B44
004ECDF2  ucomiss  xmm5, xmm9
004ECDF6  movss    dword ptr [rip + 0x1b77d36], xmm1  ; -> 02064B34
004ECDFE  movss    dword ptr [rip + 0x1b77d4e], xmm0  ; -> 02064B54
004ECE06  movss    dword ptr [rip + 0x1b77d22], xmm5  ; -> 02064B30
004ECE0E  jp       0x4ece12  ; -> 004ECE12
004ECE10  je       0x4ece1a  ; -> 004ECE1A
004ECE12  ucomiss  xmm1, xmm9
004ECE16  jp       0x4ece2f  ; -> 004ECE2F
004ECE18  jne      0x4ece2f  ; -> 004ECE2F
004ECE1A  call     0x22cc40  ; -> 0022CC40 fn
004ECE1F  movss    xmm1, dword ptr [rip + 0x1b77d0d]  ; -> 02064B34
004ECE27  movss    xmm5, dword ptr [rip + 0x1b77d01]  ; -> 02064B30
004ECE2F  comiss   xmm9, xmm5
004ECE33  ja       0x4ece3b  ; -> 004ECE3B
004ECE35  comiss   xmm9, xmm1
004ECE39  jbe      0x4ece40  ; -> 004ECE40
004ECE3B  call     0x22cc30  ; -> 0022CC30 fn
004ECE40  call     0x22cc20  ; -> 0022CC20 fn
004ECE45  movss    xmm2, dword ptr [rip + 0x1b77cf3]  ; -> 02064B40
004ECE4D  movss    xmm0, dword ptr [rip + 0x1b77d43]  ; -> 02064B98
004ECE55  addss    xmm2, xmm2
004ECE59  movss    xmm1, dword ptr [rip + 0x1b77d3b]  ; -> 02064B9C
004ECE61  subss    xmm0, dword ptr [rip + 0x1b77d27]  ; -> 02064B90
004ECE69  subss    xmm1, dword ptr [rip + 0x1b77d23]  ; -> 02064B94
004ECE71  movss    xmm4, dword ptr [rip + 0x1b77ccb]  ; -> 02064B44
004ECE79  ucomiss  xmm2, xmm9
004ECE7D  movss    xmm5, dword ptr [rip + 0x19159b7]  ; -> 01E0283C [f32 1]
004ECE85  addss    xmm4, xmm4
004ECE89  movss    xmm6, dword ptr [rip + 0x4134cf]  ; -> 00900360 [u32 0x7F7FFFFF]
004ECE91  movss    dword ptr [rip + 0x1b77d0f], xmm0  ; -> 02064BA8
004ECE99  movss    dword ptr [rip + 0x1b77d0b], xmm1  ; -> 02064BAC
004ECEA1  jp       0x4eceaa  ; -> 004ECEAA
004ECEA3  jne      0x4eceaa  ; -> 004ECEAA
004ECEA5  movaps   xmm1, xmm6
004ECEA8  jmp      0x4eceb1  ; -> 004ECEB1
004ECEAA  movaps   xmm1, xmm5
004ECEAD  divss    xmm1, xmm2
004ECEB1  ucomiss  xmm4, xmm9
004ECEB5  movss    xmm3, dword ptr [rip + 0x1915973]  ; -> 01E02830 [u32 0x00000000]
004ECEBD  movaps   xmm0, xmm3
004ECEC0  addss    xmm0, xmm1
004ECEC4  movss    dword ptr [rip + 0x1b77c74], xmm0  ; -> 02064B40
004ECECC  jp       0x4ecedd  ; -> 004ECEDD
004ECECE  jne      0x4ecedd  ; -> 004ECEDD
004ECED0  movss    dword ptr [rip + 0x1b77c28], xmm6  ; -> 02064B00
004ECED8  movaps   xmm0, xmm6
004ECEDB  jmp      0x4eceec  ; -> 004ECEEC
004ECEDD  movaps   xmm0, xmm5
004ECEE0  divss    xmm0, xmm4
004ECEE4  movss    dword ptr [rip + 0x1b77c14], xmm0  ; -> 02064B00
004ECEEC  movss    xmm2, dword ptr [rip + 0x1915940]  ; -> 01E02834 [u32 0x00000000]
004ECEF4  movaps   xmm1, xmm2
004ECEF7  addss    xmm1, xmm0
004ECEFB  ucomiss  xmm1, xmm9
004ECEFF  movss    dword ptr [rip + 0x1b77c3d], xmm1  ; -> 02064B44
004ECF07  jp       0x4ecf30  ; -> 004ECF30
004ECF09  jne      0x4ecf30  ; -> 004ECF30
004ECF0B  call     0x22cc40  ; -> 0022CC40 fn
004ECF10  movss    xmm1, dword ptr [rip + 0x1b77c2c]  ; -> 02064B44
004ECF18  movss    xmm5, dword ptr [rip + 0x191591c]  ; -> 01E0283C [f32 1]
004ECF20  movss    xmm2, dword ptr [rip + 0x191590c]  ; -> 01E02834 [u32 0x00000000]
004ECF28  movss    xmm3, dword ptr [rip + 0x1915900]  ; -> 01E02830 [u32 0x00000000]
004ECF30  comiss   xmm9, xmm1
004ECF34  jbe      0x4ecf53  ; -> 004ECF53
004ECF36  call     0x22cc30  ; -> 0022CC30 fn
004ECF3B  movss    xmm5, dword ptr [rip + 0x19158f9]  ; -> 01E0283C [f32 1]
004ECF43  movss    xmm2, dword ptr [rip + 0x19158e9]  ; -> 01E02834 [u32 0x00000000]
004ECF4B  movss    xmm3, dword ptr [rip + 0x19158dd]  ; -> 01E02830 [u32 0x00000000]
004ECF53  movzx    ecx, word ptr [rip + 0x1b77bb2]  ; -> 02064B0C
004ECF5A  movaps   xmm0, xmm3
004ECF5D  addss    xmm0, dword ptr [rip + 0x1b77c43]  ; -> 02064BA8
004ECF65  mov      word ptr [rip + 0x1b77e4c], cx  ; -> 02064DB8
004ECF6C  addss    xmm3, xmm5
004ECF70  movaps   xmm1, xmm2
004ECF73  mov      dword ptr [rip + 0x1b77b7f], 1  ; -> 02064AFC
004ECF7D  addss    xmm1, dword ptr [rip + 0x1b77c27]  ; -> 02064BAC
004ECF85  lea      eax, [rcx + 0x40]
004ECF88  add      cx, 8
004ECF8C  mov      word ptr [rip + 0x1b77e3d], cx  ; -> 02064DD0
004ECF93  addss    xmm2, xmm2
004ECF97  mov      word ptr [rip + 0x1b77e12], ax  ; -> 02064DB0
004ECF9E  inc      ax
004ECFA1  mov      word ptr [rip + 0x1b77e0c], ax  ; -> 02064DB4
004ECFA8  movss    dword ptr [rip + 0x1b77bf0], xmm0  ; -> 02064BA0
004ECFB0  movss    xmm0, dword ptr [rip + 0x1b77b84]  ; -> 02064B3C
004ECFB8  movss    dword ptr [rip + 0x1915868], xmm0  ; -> 01E02828 [f32 1]
004ECFC0  mov      eax, dword ptr [rip + 0x1915862]  ; -> 01E02828 [f32 1]
004ECFC6  mov      ecx, eax
004ECFC8  shr      ecx, 0x12
004ECFCB  xor      ecx, eax
004ECFCD  movss    dword ptr [rip + 0x1b77bcf], xmm1  ; -> 02064BA4
004ECFD5  and      eax, 0x3fffff
004ECFDA  shr      ecx, 4
004ECFDD  or       eax, 0x1fc00000
004ECFE2  movss    dword ptr [rip + 0x1b77bd6], xmm3  ; -> 02064BC0
004ECFEA  add      eax, eax
004ECFEC  movss    dword ptr [rip + 0x1b77bd0], xmm2  ; -> 02064BC4
004ECFF4  and      ecx, 1
004ECFF7  or       ecx, eax
004ECFF9  mov      dword ptr [rip + 0x1915829], ecx  ; -> 01E02828 [f32 1]
004ECFFF  movss    xmm0, dword ptr [rip + 0x1915821]  ; -> 01E02828 [f32 1]
004ED007  movss    dword ptr [rip + 0x1b77ca1], xmm0  ; -> 02064CB0
004ED00F  call     0x5375f0  ; -> 005375F0 fn
004ED014  call     0x5376d0  ; -> 005376D0 fn
004ED019  movss    xmm0, dword ptr [rip + 0x1b77ca3]  ; -> 02064CC4
004ED021  movss    xmm2, dword ptr [rip + 0x1915807]  ; -> 01E02830 [u32 0x00000000]
004ED029  movss    xmm1, dword ptr [rip + 0x1b77c8f]  ; -> 02064CC0
004ED031  addss    xmm0, xmm2
004ED035  subss    xmm2, xmm1
004ED039  movss    dword ptr [rip + 0x1b77cbf], xmm0  ; -> 02064D00
004ED041  movaps   xmm0, xmm1
004ED044  addss    xmm0, dword ptr [rip + 0x19157e8]  ; -> 01E02834 [u32 0x00000000]
004ED04C  movss    dword ptr [rip + 0x1b77cbc], xmm2  ; -> 02064D10
004ED054  movss    dword ptr [rip + 0x1b77ca8], xmm0  ; -> 02064D04
004ED05C  call     0x22cc20  ; -> 0022CC20 fn
004ED061  movss    xmm0, dword ptr [rip + 0x1b77ca7]  ; -> 02064D10
004ED069  mulss    xmm0, dword ptr [rip + 0x1b77b53]  ; -> 02064BC4
004ED071  movsx    eax, word ptr [rip + 0x1b77a94]  ; -> 02064B0C
004ED078  movss    xmm2, dword ptr [rip + 0x1b77c80]  ; -> 02064D00
004ED080  add      eax, 2
004ED083  mulss    xmm2, dword ptr [rip + 0x1b77b35]  ; -> 02064BC0
004ED08B  shl      eax, 4
004ED08E  movss    xmm4, dword ptr [rip + 0x1b77c2e]  ; -> 02064CC4
004ED096  addss    xmm4, dword ptr [rip + 0x1915796]  ; -> 01E02834 [u32 0x00000000]
004ED09E  movss    xmm3, dword ptr [rip + 0x1b77c5e]  ; -> 02064D04
004ED0A6  addss    xmm0, xmm2
004ED0AA  mulss    xmm3, dword ptr [rip + 0x1b77b0e]  ; -> 02064BC0
004ED0B2  cdqe     
004ED0B4  movss    dword ptr [rip + 0x1b77a64], xmm2  ; -> 02064B20
004ED0BC  movss    dword ptr [rip + 0x1b77c50], xmm4  ; -> 02064D14
004ED0C4  mulss    xmm4, dword ptr [rip + 0x1b77af8]  ; -> 02064BC4
004ED0CC  movss    dword ptr [rip + 0x1b77aec], xmm0  ; -> 02064BC0
004ED0D4  movss    xmm0, dword ptr [rax + rsi]
004ED0D9  movss    dword ptr [rip + 0x1b77bcf], xmm0  ; -> 02064CB0
004ED0E1  addss    xmm4, xmm3
004ED0E5  movd     xmm1, dword ptr [rip + 0x1b77bc3]  ; -> 02064CB0
004ED0ED  cvtdq2ps xmm1, xmm1
004ED0F0  movss    dword ptr [rip + 0x1b77a2c], xmm3  ; -> 02064B24
004ED0F8  ucomiss  xmm1, xmm9
004ED0FC  movss    dword ptr [rip + 0x1b77ac0], xmm4  ; -> 02064BC4
004ED104  jp       0x4ed108  ; -> 004ED108
004ED106  je       0x4ed114  ; -> 004ED114
004ED108  movss    xmm6, dword ptr [rip + 0x1b77a28]  ; -> 02064B38
004ED110  divss    xmm6, xmm1
004ED114  movss    xmm0, dword ptr [rip + 0x1915714]  ; -> 01E02830 [u32 0x00000000]
004ED11C  addss    xmm0, xmm6
004ED120  movss    dword ptr [rip + 0x1b779d8], xmm6  ; -> 02064B00
004ED128  movss    dword ptr [rip + 0x1b77b80], xmm0  ; -> 02064CB0
004ED130  call     0x5375f0  ; -> 005375F0 fn
004ED135  call     0x5376d0  ; -> 005376D0 fn
004ED13A  movss    xmm0, dword ptr [rip + 0x1b77b82]  ; -> 02064CC4
004ED142  movss    xmm2, dword ptr [rip + 0x19156e6]  ; -> 01E02830 [u32 0x00000000]
004ED14A  movss    xmm1, dword ptr [rip + 0x1b77b6e]  ; -> 02064CC0
004ED152  addss    xmm0, xmm2
004ED156  subss    xmm2, xmm1
004ED15A  movss    dword ptr [rip + 0x1b77b9e], xmm0  ; -> 02064D00
004ED162  movaps   xmm0, xmm1
004ED165  addss    xmm0, dword ptr [rip + 0x19156c7]  ; -> 01E02834 [u32 0x00000000]
004ED16D  movss    dword ptr [rip + 0x1b77b9b], xmm2  ; -> 02064D10
004ED175  movss    dword ptr [rip + 0x1b77b87], xmm0  ; -> 02064D04
004ED17D  call     0x22cc20  ; -> 0022CC20 fn
004ED182  movss    xmm10, dword ptr [rip + 0x1b77b39]  ; -> 02064CC4
004ED18B  addss    xmm10, dword ptr [rip + 0x19156a0]  ; -> 01E02834 [u32 0x00000000]
004ED194  movaps   xmm15, xmmword ptr [rip + 0x428254]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004ED19C  movss    xmm14, dword ptr [rip + 0x17fea03]  ; -> 01CEBBA8 [f32 1]
004ED1A5  movzx    eax, word ptr [rip + 0x1b77c10]  ; -> 02064DBC
004ED1AC  movzx    ecx, word ptr [rip + 0x1b77c05]  ; -> 02064DB8
004ED1B3  movss    dword ptr [rip + 0x1b77b58], xmm10  ; -> 02064D14
004ED1BC  nop      dword ptr [rax]
004ED1C0  mulss    xmm10, dword ptr [rip + 0x1b779fb]  ; -> 02064BC4
004ED1C9  dec      ax
004ED1CC  inc      cx
004ED1CF  mov      word ptr [rip + 0x1b77be6], ax  ; -> 02064DBC
004ED1D6  movss    xmm1, dword ptr [rip + 0x1b77b22]  ; -> 02064D00
004ED1DE  cmp      dword ptr [rip + 0x1b77917], 0  ; -> 02064AFC
004ED1E5  mulss    xmm1, dword ptr [rip + 0x1b779d3]  ; -> 02064BC0
004ED1ED  mov      word ptr [rip + 0x1b77bc4], cx  ; -> 02064DB8
004ED1F4  movss    xmm2, dword ptr [rip + 0x1b77b08]  ; -> 02064D04
004ED1FC  mulss    xmm2, dword ptr [rip + 0x1b779bc]  ; -> 02064BC0
004ED204  movss    xmm11, dword ptr [rip + 0x1b77b03]  ; -> 02064D10
004ED20D  mulss    xmm11, dword ptr [rip + 0x1b779ae]  ; -> 02064BC4
004ED216  addss    xmm10, xmm2
004ED21B  movss    dword ptr [rip + 0x1b778fd], xmm1  ; -> 02064B20
004ED223  movss    dword ptr [rip + 0x1b778f9], xmm2  ; -> 02064B24
004ED22B  addss    xmm11, xmm1
004ED230  movss    dword ptr [rip + 0x1b7798b], xmm10  ; -> 02064BC4
004ED239  movss    dword ptr [rip + 0x1b7797e], xmm11  ; -> 02064BC0
004ED242  je       0x4ed4bc  ; -> 004ED4BC
004ED248  mov      eax, dword ptr [rip + 0x19155da]  ; -> 01E02828 [f32 1]
004ED24E  mov      ecx, eax
004ED250  shr      ecx, 0x12
004ED253  xor      ecx, eax
004ED255  and      eax, 0x3fffff
004ED25A  shr      ecx, 4
004ED25D  or       eax, 0x1fc00000
004ED262  and      ecx, 1
004ED265  add      eax, eax
004ED267  or       ecx, eax
004ED269  mov      eax, ecx
004ED26B  shr      eax, 0x12
004ED26E  xor      eax, ecx
004ED270  and      ecx, 0x3fffff
004ED276  or       ecx, 0x1fc00000
004ED27C  shr      eax, 4
004ED27F  add      ecx, ecx
004ED281  and      eax, 1
004ED284  or       eax, ecx
004ED286  mov      ecx, eax
004ED288  shr      ecx, 0x12
004ED28B  xor      ecx, eax
004ED28D  and      eax, 0x3fffff
004ED292  shr      ecx, 4
004ED295  or       eax, 0x1fc00000
004ED29A  and      ecx, 1
004ED29D  add      eax, eax
004ED29F  or       ecx, eax
004ED2A1  mov      eax, ecx
004ED2A3  shr      eax, 0x12
004ED2A6  xor      eax, ecx
004ED2A8  and      ecx, 0x3fffff
004ED2AE  or       ecx, 0x1fc00000
004ED2B4  shr      eax, 4
004ED2B7  add      ecx, ecx
004ED2B9  and      eax, 1
004ED2BC  or       eax, ecx
004ED2BE  mov      ecx, eax
004ED2C0  shr      ecx, 0x12
004ED2C3  xor      ecx, eax
004ED2C5  and      eax, 0x3fffff
004ED2CA  shr      ecx, 4
004ED2CD  or       eax, 0x1fc00000
004ED2D2  and      ecx, 1
004ED2D5  add      eax, eax
004ED2D7  or       ecx, eax
004ED2D9  mov      eax, ecx
004ED2DB  mov      dword ptr [rip + 0x1915547], ecx  ; -> 01E02828 [f32 1]
004ED2E1  movss    xmm4, dword ptr [rip + 0x191553f]  ; -> 01E02828 [f32 1]
004ED2E9  shr      eax, 0x12
004ED2EC  xor      eax, ecx
004ED2EE  and      ecx, 0x3fffff
004ED2F4  or       ecx, 0x1fc00000
004ED2FA  shr      eax, 4
004ED2FD  add      ecx, ecx
004ED2FF  and      eax, 1
004ED302  or       eax, ecx
004ED304  mov      ecx, eax
004ED306  shr      ecx, 0x12
004ED309  xor      ecx, eax
004ED30B  and      eax, 0x3fffff
004ED310  shr      ecx, 4
004ED313  or       eax, 0x1fc00000
004ED318  and      ecx, 1
004ED31B  add      eax, eax
004ED31D  or       ecx, eax
004ED31F  mov      eax, ecx
004ED321  shr      eax, 0x12
004ED324  xor      eax, ecx
004ED326  and      ecx, 0x3fffff
004ED32C  or       ecx, 0x1fc00000
004ED332  shr      eax, 4
004ED335  add      ecx, ecx
004ED337  and      eax, 1
004ED33A  or       eax, ecx
004ED33C  mov      ecx, eax
004ED33E  shr      ecx, 0x12
004ED341  xor      ecx, eax
004ED343  shr      ecx, 4
004ED346  and      ecx, 1
004ED349  and      eax, 0x3fffff
004ED34E  or       eax, 0x1fc00000
004ED353  add      eax, eax
004ED355  or       ecx, eax
004ED357  mov      edx, ecx
004ED359  shr      edx, 0x12
004ED35C  xor      edx, ecx
004ED35E  and      ecx, 0x3fffff
004ED364  or       ecx, 0x1fc00000
004ED36A  shr      edx, 4
004ED36D  add      ecx, ecx
004ED36F  and      edx, 1
004ED372  or       edx, ecx
004ED374  mov      dword ptr [rip + 0x19154ae], edx  ; -> 01E02828 [f32 1]
004ED37A  mov      eax, edx
004ED37C  movss    xmm3, dword ptr [rip + 0x19154a4]  ; -> 01E02828 [f32 1]
004ED384  shr      eax, 0x12
004ED387  xor      eax, edx
004ED389  and      edx, 0x3fffff
004ED38F  shr      eax, 4
004ED392  or       edx, 0x1fc00000
004ED398  and      eax, 1
004ED39B  add      edx, edx
004ED39D  or       eax, edx
004ED39F  mov      ecx, eax
004ED3A1  shr      ecx, 0x12
004ED3A4  xor      ecx, eax
004ED3A6  and      eax, 0x3fffff
004ED3AB  or       eax, 0x1fc00000
004ED3B0  shr      ecx, 4
004ED3B3  add      eax, eax
004ED3B5  and      ecx, 1
004ED3B8  or       ecx, eax
004ED3BA  mov      eax, ecx
004ED3BC  shr      eax, 0x12
004ED3BF  xor      eax, ecx
004ED3C1  and      ecx, 0x3fffff
004ED3C7  or       ecx, 0x1fc00000
004ED3CD  shr      eax, 4
004ED3D0  add      ecx, ecx
004ED3D2  and      eax, 1
004ED3D5  or       eax, ecx
004ED3D7  mov      ecx, eax
004ED3D9  shr      ecx, 0x12
004ED3DC  xor      ecx, eax
004ED3DE  and      eax, 0x3fffff
004ED3E3  or       eax, 0x1fc00000
004ED3E8  shr      ecx, 4
004ED3EB  add      eax, eax
004ED3ED  and      ecx, 1
004ED3F0  or       ecx, eax
004ED3F2  mov      edx, ecx
004ED3F4  shr      edx, 0x12
004ED3F7  xor      edx, ecx
004ED3F9  and      ecx, 0x3fffff
004ED3FF  or       ecx, 0x1fc00000
004ED405  shr      edx, 4
004ED408  add      ecx, ecx
004ED40A  and      edx, 1
004ED40D  or       edx, ecx
004ED40F  mov      eax, edx
004ED411  mov      dword ptr [rip + 0x1915411], edx  ; -> 01E02828 [f32 1]
004ED417  movss    xmm12, dword ptr [rip + 0x1915408]  ; -> 01E02828 [f32 1]
004ED420  shr      eax, 0x12
004ED423  xor      eax, edx
004ED425  and      edx, 0x3fffff
004ED42B  shr      eax, 4
004ED42E  or       edx, 0x1fc00000
004ED434  and      eax, 1
004ED437  add      edx, edx
004ED439  or       eax, edx
004ED43B  mov      ecx, eax
004ED43D  shr      ecx, 0x12
004ED440  xor      ecx, eax
004ED442  and      eax, 0x3fffff
004ED447  or       eax, 0x1fc00000
004ED44C  shr      ecx, 4
004ED44F  add      eax, eax
004ED451  and      ecx, 1
004ED454  or       ecx, eax
004ED456  mov      eax, ecx
004ED458  shr      eax, 0x12
004ED45B  xor      eax, ecx
004ED45D  and      ecx, 0x3fffff
004ED463  or       ecx, 0x1fc00000
004ED469  shr      eax, 4
004ED46C  add      ecx, ecx
004ED46E  and      eax, 1
004ED471  or       eax, ecx
004ED473  mov      ecx, eax
004ED475  shr      ecx, 0x12
004ED478  xor      ecx, eax
004ED47A  and      eax, 0x3fffff
004ED47F  or       eax, 0x1fc00000
004ED484  shr      ecx, 4
004ED487  add      eax, eax
004ED489  and      ecx, 1
004ED48C  or       ecx, eax
004ED48E  mov      eax, ecx
004ED490  shr      eax, 0x12
004ED493  xor      eax, ecx
004ED495  and      ecx, 0x3fffff
004ED49B  or       ecx, 0x1fc00000
004ED4A1  shr      eax, 4
004ED4A4  add      ecx, ecx
004ED4A6  and      eax, 1
004ED4A9  or       eax, ecx
004ED4AB  mov      dword ptr [rip + 0x1915377], eax  ; -> 01E02828 [f32 1]
004ED4B1  movss    xmm13, dword ptr [rip + 0x191536e]  ; -> 01E02828 [f32 1]
004ED4BA  jmp      0x4ed4cc  ; -> 004ED4CC
004ED4BC  movaps   xmm4, xmm14
004ED4C0  movaps   xmm3, xmm14
004ED4C4  movaps   xmm12, xmm14
004ED4C8  movaps   xmm13, xmm14
004ED4CC  movss    xmm8, dword ptr [rip + 0x1915367]  ; -> 01E0283C [f32 1]
004ED4D5  movaps   xmm5, xmm11
004ED4D9  movss    xmm2, dword ptr [rip + 0x1915357]  ; -> 01E02838 [u32 0x00000000]
004ED4E1  subss    xmm3, xmm8
004ED4E6  movaps   xmm0, xmm2
004ED4E9  subss    xmm4, xmm8
004ED4EE  addss    xmm0, dword ptr [rip + 0x1b77652]  ; -> 02064B48
004ED4F6  addss    xmm2, xmm8
004ED4FB  movaps   xmm7, xmm11
004ED4FF  movaps   xmm6, xmm10
004ED503  subss    xmm12, xmm8
004ED508  mulss    xmm3, dword ptr [rip + 0x1b77654]  ; -> 02064B64
004ED510  subss    xmm13, xmm8
004ED515  movss    dword ptr [rip + 0x1b776cb], xmm0  ; -> 02064BE8
004ED51D  movaps   xmm1, xmm8
004ED521  movss    dword ptr [rip + 0x1b776df], xmm0  ; -> 02064C08
004ED529  movss    xmm0, dword ptr [rip + 0x1b7762b]  ; -> 02064B5C
004ED531  mulss    xmm0, xmm4
004ED535  movaps   xmm4, xmm10
004ED539  mulss    xmm4, xmm3
004ED53D  mulss    xmm7, xmm0
004ED541  mulss    xmm6, xmm0
004ED545  mulss    xmm1, xmm8
004ED54A  mulss    xmm5, xmm3
004ED54E  movaps   xmm3, xmm10
004ED552  mulss    xmm3, dword ptr [rip + 0x1b775fe]  ; -> 02064B58
004ED55A  movss    dword ptr [rip + 0x1b7768a], xmm1  ; -> 02064BEC
004ED562  movss    dword ptr [rip + 0x1b776a2], xmm1  ; -> 02064C0C
004ED56A  movss    xmm1, dword ptr [rip + 0x1b775ee]  ; -> 02064B60
004ED572  addss    xmm6, xmm3
004ED576  movaps   xmm0, xmm1
004ED579  movss    dword ptr [rip + 0x1b77657], xmm2  ; -> 02064BD8
004ED581  mulss    xmm0, xmm11
004ED586  mulss    xmm1, xmm10
004ED58B  addss    xmm5, xmm0
004ED58F  movss    dword ptr [rip + 0x1b77661], xmm2  ; -> 02064BF8
004ED597  movss    dword ptr [rip + 0x1b77721], xmm0  ; -> 02064CC0
004ED59F  movaps   xmm10, xmm6
004ED5A3  movss    xmm0, dword ptr [rip + 0x1b775a5]  ; -> 02064B50
004ED5AB  addss    xmm4, xmm1
004ED5AF  movaps   xmm2, xmm11
004ED5B3  movss    dword ptr [rip + 0x1b77709], xmm1  ; -> 02064CC4
004ED5BB  mulss    xmm2, dword ptr [rip + 0x1b77595]  ; -> 02064B58
004ED5C3  movss    xmm1, dword ptr [rip + 0x1b77589]  ; -> 02064B54
004ED5CB  movss    dword ptr [rip + 0x1b776e1], xmm3  ; -> 02064CB4
004ED5D3  addss    xmm6, xmm1
004ED5D7  addss    xmm7, xmm2
004ED5DB  movss    dword ptr [rip + 0x1b776cd], xmm2  ; -> 02064CB0
004ED5E3  movss    dword ptr [rip + 0x1b776e4], xmm12  ; -> 02064CD0
004ED5EC  movaps   xmm3, xmm5
004ED5EF  mulss    xmm12, dword ptr [rip + 0x1b77570]  ; -> 02064B68
004ED5F8  addss    xmm5, xmm0
004ED5FC  movss    dword ptr [rip + 0x1b776db], xmm13  ; -> 02064CE0
004ED605  movaps   xmm2, xmm4
004ED608  mulss    xmm13, dword ptr [rip + 0x1b7755b]  ; -> 02064B6C
004ED611  addss    xmm4, xmm1
004ED615  addss    xmm12, xmm8
004ED61A  movss    dword ptr [rip + 0x1b775c2], xmm6  ; -> 02064BE4
004ED622  movaps   xmm11, xmm7
004ED626  movss    dword ptr [rip + 0x1b775d2], xmm5  ; -> 02064C00
004ED62E  addss    xmm7, xmm0
004ED632  addss    xmm13, xmm8
004ED637  movss    dword ptr [rip + 0x1b775c5], xmm4  ; -> 02064C04
004ED63F  mulss    xmm11, xmm12
004ED644  movss    dword ptr [rip + 0x1b77594], xmm7  ; -> 02064BE0
004ED64C  mulss    xmm3, xmm13
004ED651  addss    xmm11, xmm0
004ED656  mulss    xmm10, xmm12
004ED65B  addss    xmm3, xmm0
004ED65F  mulss    xmm2, xmm13
004ED664  movups   xmm0, xmmword ptr [rip + 0x1b77575]  ; -> 02064BE0
004ED66B  addss    xmm2, xmm1
004ED66F  mulps    xmm0, xmm15
004ED673  addss    xmm10, xmm1
004ED678  movups   xmm1, xmmword ptr [rip + 0x1b77581]  ; -> 02064C00
004ED67F  movss    dword ptr [rip + 0x1b77569], xmm3  ; -> 02064BF0
004ED687  cvttps2dq xmm0, xmm0
004ED68B  mulps    xmm1, xmm15
004ED68F  movdqu   xmmword ptr [rip + 0x1b77549], xmm0  ; -> 02064BE0
004ED697  movss    dword ptr [rip + 0x1b77555], xmm2  ; -> 02064BF4
004ED69F  cvttps2dq xmm0, xmm1
004ED6A3  subss    xmm11, dword ptr [rip + 0x1b77484]  ; -> 02064B30
004ED6AC  subss    xmm10, dword ptr [rip + 0x1b7747f]  ; -> 02064B34
004ED6B5  movdqu   xmmword ptr [rip + 0x1b77543], xmm0  ; -> 02064C00
004ED6BD  ucomiss  xmm11, xmm9
004ED6C1  movss    dword ptr [rip + 0x1b77506], xmm11  ; -> 02064BD0
004ED6CA  movss    dword ptr [rip + 0x1b77501], xmm10  ; -> 02064BD4
004ED6D3  jp       0x4ed6d7  ; -> 004ED6D7
004ED6D5  je       0x4ed6df  ; -> 004ED6DF
004ED6D7  ucomiss  xmm10, xmm9
004ED6DB  jp       0x4ed6f6  ; -> 004ED6F6
004ED6DD  jne      0x4ed6f6  ; -> 004ED6F6
004ED6DF  call     0x22cc40  ; -> 0022CC40 fn
004ED6E4  movss    xmm10, dword ptr [rip + 0x1b774e7]  ; -> 02064BD4
004ED6ED  movss    xmm11, dword ptr [rip + 0x1b774da]  ; -> 02064BD0
004ED6F6  comiss   xmm9, xmm11
004ED6FA  ja       0x4ed702  ; -> 004ED702
004ED6FC  comiss   xmm9, xmm10
004ED700  jbe      0x4ed707  ; -> 004ED707
004ED702  call     0x22cc30  ; -> 0022CC30 fn
004ED707  call     0x22cc20  ; -> 0022CC20 fn
004ED70C  movss    xmm1, dword ptr [rip + 0x1b774dc]  ; -> 02064BF0
004ED714  movss    xmm0, dword ptr [rip + 0x1b774d8]  ; -> 02064BF4
004ED71C  subss    xmm1, dword ptr [rip + 0x1b7740c]  ; -> 02064B30
004ED724  subss    xmm0, dword ptr [rip + 0x1b77408]  ; -> 02064B34
004ED72C  ucomiss  xmm1, xmm9
004ED730  movss    dword ptr [rip + 0x1b774b8], xmm1  ; -> 02064BF0
004ED738  movss    dword ptr [rip + 0x1b774b4], xmm0  ; -> 02064BF4
004ED740  jp       0x4ed744  ; -> 004ED744
004ED742  je       0x4ed74c  ; -> 004ED74C
004ED744  ucomiss  xmm0, xmm9
004ED748  jp       0x4ed761  ; -> 004ED761
004ED74A  jne      0x4ed761  ; -> 004ED761
004ED74C  call     0x22cc40  ; -> 0022CC40 fn
004ED751  movss    xmm0, dword ptr [rip + 0x1b7749b]  ; -> 02064BF4
004ED759  movss    xmm1, dword ptr [rip + 0x1b7748f]  ; -> 02064BF0
004ED761  comiss   xmm9, xmm1
004ED765  ja       0x4ed76d  ; -> 004ED76D
004ED767  comiss   xmm9, xmm0
004ED76B  jbe      0x4ed772  ; -> 004ED772
004ED76D  call     0x22cc30  ; -> 0022CC30 fn
004ED772  call     0x22cc20  ; -> 0022CC20 fn
004ED777  movsx    edx, word ptr [rip + 0x1b77636]  ; -> 02064DB4
004ED77E  movss    xmm5, dword ptr [rip + 0x1b7744a]  ; -> 02064BD0
004ED786  mov      eax, edx
004ED788  movss    xmm6, dword ptr [rip + 0x1b77444]  ; -> 02064BD4
004ED790  inc      dx
004ED793  mulss    xmm5, dword ptr [rip + 0x1b773a5]  ; -> 02064B40
004ED79B  shl      eax, 4
004ED79E  mulss    xmm6, dword ptr [rip + 0x1b7739e]  ; -> 02064B44
004ED7A6  movsxd   rcx, eax
004ED7A9  movss    xmm3, dword ptr [rip + 0x1b7743f]  ; -> 02064BF0
004ED7B1  movss    xmm4, dword ptr [rip + 0x1b7743b]  ; -> 02064BF4
004ED7B9  mulss    xmm3, dword ptr [rip + 0x1b7737f]  ; -> 02064B40
004ED7C1  movsx    eax, dx
004ED7C4  inc      dx
004ED7C7  mulss    xmm4, dword ptr [rip + 0x1b77375]  ; -> 02064B44
004ED7CF  shl      eax, 4
004ED7D2  mulss    xmm5, dword ptr [rip + 0x1b773c6]  ; -> 02064BA0
004ED7DA  mulss    xmm6, dword ptr [rip + 0x1b773c2]  ; -> 02064BA4
004ED7E2  addss    xmm5, dword ptr [rip + 0x1b773a6]  ; -> 02064B90
004ED7EA  mulss    xmm3, dword ptr [rip + 0x1b773ae]  ; -> 02064BA0
004ED7F2  addss    xmm6, dword ptr [rip + 0x1b7739a]  ; -> 02064B94
004ED7FA  mulss    xmm4, dword ptr [rip + 0x1b773a2]  ; -> 02064BA4
004ED802  addss    xmm3, dword ptr [rip + 0x1b77386]  ; -> 02064B90
004ED80A  movss    dword ptr [rip + 0x1b773be], xmm5  ; -> 02064BD0
004ED812  addss    xmm4, dword ptr [rip + 0x1b7737a]  ; -> 02064B94
004ED81A  movss    dword ptr [rip + 0x1b773b2], xmm6  ; -> 02064BD4
004ED822  movups   xmm0, xmmword ptr [rip + 0x1b773a7]  ; -> 02064BD0
004ED829  movss    dword ptr [rip + 0x1b773bf], xmm3  ; -> 02064BF0
004ED831  movups   xmmword ptr [rcx + rsi], xmm0
004ED835  movsxd   rcx, eax
004ED838  movups   xmm0, xmmword ptr [rip + 0x1b77331]  ; -> 02064B70
004ED83F  movsx    eax, dx
004ED842  inc      dx
004ED845  shl      eax, 4
004ED848  movups   xmmword ptr [rcx + rsi], xmm0
004ED84C  movsxd   rcx, eax
004ED84F  movups   xmm0, xmmword ptr [rip + 0x1b7738a]  ; -> 02064BE0
004ED856  movsx    eax, dx
004ED859  inc      dx
004ED85C  shl      eax, 4
004ED85F  movups   xmmword ptr [rcx + rsi], xmm0
004ED863  movsxd   rcx, eax
004ED866  movsx    eax, dx
004ED869  inc      dx
004ED86C  shl      eax, 4
004ED86F  movss    dword ptr [rip + 0x1b7737d], xmm4  ; -> 02064BF4
004ED877  movups   xmm0, xmmword ptr [rip + 0x1b77372]  ; -> 02064BF0
004ED87E  movups   xmmword ptr [rcx + rsi], xmm0
004ED882  movsxd   rcx, eax
004ED885  movups   xmm0, xmmword ptr [rip + 0x1b772f4]  ; -> 02064B80
004ED88C  movsx    eax, dx
004ED88F  inc      dx
004ED892  shl      eax, 4
004ED895  movups   xmmword ptr [rcx + rsi], xmm0
004ED899  movzx    ecx, word ptr [rip + 0x1b77518]  ; -> 02064DB8
004ED8A0  movups   xmm0, xmmword ptr [rip + 0x1b77359]  ; -> 02064C00
004ED8A7  cdqe     
004ED8A9  mov      word ptr [rip + 0x1b77504], dx  ; -> 02064DB4
004ED8B0  movzx    edx, word ptr [rip + 0x1b77255]  ; -> 02064B0C
004ED8B7  movups   xmmword ptr [rax + rsi], xmm0
004ED8BB  lea      eax, [rdx + 0x40]
004ED8BE  mov      word ptr [rip + 0x1b7750f], ax  ; -> 02064DD4
004ED8C5  cmp      cx, ax
004ED8C8  jne      0x4ed8e3  ; -> 004ED8E3
004ED8CA  mov      rdx, rbx
004ED8CD  mov      rcx, rdi
004ED8D0  call     0x4ecb70  ; -> 004ECB70 fn
004ED8D5  movzx    edx, word ptr [rip + 0x1b77230]  ; -> 02064B0C
004ED8DC  movzx    ecx, word ptr [rip + 0x1b774d5]  ; -> 02064DB8
004ED8E3  movzx    eax, word ptr [rip + 0x1b774d2]  ; -> 02064DBC
004ED8EA  cmp      ax, dx
004ED8ED  je       0x4ed8fd  ; -> 004ED8FD
004ED8EF  movss    xmm10, dword ptr [rip + 0x1b7741c]  ; -> 02064D14
004ED8F8  jmp      0x4ed1c0  ; -> 004ED1C0
004ED8FD  cmp      cx, dx
004ED900  je       0x4ed90d  ; -> 004ED90D
004ED902  mov      rdx, rbx
004ED905  mov      rcx, rdi
004ED908  call     0x4ecb70  ; -> 004ECB70 fn
004ED90D  movaps   xmm14, xmmword ptr [rsp + 0x40]
004ED913  lea      r11, [rsp + 0xd0]
004ED91B  mov      rbx, qword ptr [r11 + 0x10]
004ED91F  mov      rsi, qword ptr [r11 + 0x18]
004ED923  movaps   xmm6, xmmword ptr [r11 - 0x10]
004ED928  movaps   xmm7, xmmword ptr [r11 - 0x20]
004ED92D  movaps   xmm8, xmmword ptr [r11 - 0x30]
004ED932  movaps   xmm9, xmmword ptr [r11 - 0x40]
004ED937  movaps   xmm10, xmmword ptr [r11 - 0x50]
004ED93C  movaps   xmm11, xmmword ptr [r11 - 0x60]
004ED941  movaps   xmm12, xmmword ptr [r11 - 0x70]
004ED946  movaps   xmm13, xmmword ptr [r11 - 0x80]
004ED94B  movaps   xmm15, xmmword ptr [rsp + 0x30]
004ED951  mov      rsp, r11
004ED954  pop      rdi
004ED955  ret      
```

## 004FF270 (55 B, extent 004FF270-004FF2A7)

Page context: "r the chain-tracked kind: '[rcx]' byte indexes the '[[02EBEFA0]]' pointer table for the old slot 'rsi', '003A7BE0([rcx], [rcx+2], len)' allocates the replacement 'rdi', '00861EBA' copies 'r14+4' in, '004FF270' registers under '02EBB738 + rdi', then the '[[02EBEF98]]' chain is walked via '+0xF0' next pointers and every '+0xE0' field matching the old slot is repointed to the new - a copy with back-pointer fixup, returning 'r14 + 4 + len' "

```
004FF270  movzx    r8d, byte ptr [rcx + 0xc2]
004FF278  test     r8d, r8d
004FF27B  je       0x4ff2a2  ; -> 004FF2A2
004FF27D  sub      r8d, 1
004FF281  je       0x4ff29d  ; -> 004FF29D
004FF283  sub      r8d, 1
004FF287  je       0x4ff298  ; -> 004FF298
004FF289  cmp      r8d, 1
004FF28D  je       0x4ff293  ; -> 004FF293
004FF28F  mov      rax, rcx
004FF292  ret      
004FF293  jmp      0x5387b0  ; -> 005387B0 fn
004FF298  jmp      0x538350  ; -> 00538350 fn
004FF29D  jmp      0x537fa0  ; -> 00537FA0 fn
004FF2A2  jmp      0x537c80  ; -> 00537C80 fn
```

## 00501440 (108 B, extent 00501440-005014AC)

Page context: "6', a flag byte 'ptr+2 & 8' on a pointer loaded at '00500CB5'/'00503E7E' mirrors into '+0xA3 bit 0' ('00500CBC'–'00500CD2'), inner dispatch on '+0xA2' | | '0x53' | '0xC0' | '005014B0' | '00501520' | '00501440' (thunk '00501510') | string-bearing record: '001837A0'/'00183760' string helpers around '0036A100' + '00861EBA' ('0050158F' ff.); tail fixups '002D81D0', '003A22A0', '003A1DB0' | | '0x54' | '0x190' | '004354E0' | '00436D00' | '004"

```
00501440  push     rbx
00501442  sub      rsp, 0x20
00501446  mov      rbx, rcx
00501449  mov      rcx, qword ptr [rcx + 0x20]
0050144D  test     rcx, rcx
00501450  je       0x501457  ; -> 00501457
00501452  call     0x3697f0  ; -> 003697F0 fn
00501457  mov      rcx, qword ptr [rbx + 0x18]
0050145B  test     rcx, rcx
0050145E  je       0x501465  ; -> 00501465
00501460  call     0x3697f0  ; -> 003697F0 fn
00501465  mov      rcx, qword ptr [rbx + 0xb8]
0050146C  test     rcx, rcx
0050146F  je       0x50148d  ; -> 0050148D
00501471  call     0x183720  ; -> 00183720 fn
00501476  mov      rcx, qword ptr [rbx + 0xb0]
0050147D  call     0x183720  ; -> 00183720 fn
00501482  mov      qword ptr [rbx + 0xb8], 0
0050148D  mov      dword ptr [rbx + 0x10], 0
00501494  mov      dword ptr [rbx + 0xa8], 0
0050149E  mov      qword ptr [rbx + 0x20], 0
005014A6  add      rsp, 0x20
005014AA  pop      rbx
005014AB  ret      
```

## 005014B0 (94 B, extent 005014B0-0050150E)

Page context: " mirrored to '+0xA4'/'+0xA6', a flag byte 'ptr+2 & 8' on a pointer loaded at '00500CB5'/'00503E7E' mirrors into '+0xA3 bit 0' ('00500CBC'–'00500CD2'), inner dispatch on '+0xA2' | | '0x53' | '0xC0' | '005014B0' | '00501520' | '00501440' (thunk '00501510') | string-bearing record: '001837A0'/'00183760' string helpers around '0036A100' + '00861EBA' ('0050158F' ff.); tail fixups '002D81D0', '003A22A0', '003A1DB0' | | '0x54' | '0x190' | '004"

```
005014B0  mov      qword ptr [rsp + 8], rbx
005014B5  push     rdi
005014B6  sub      rsp, 0x20
005014BA  mov      rdi, rcx
005014BD  mov      rbx, rdx
005014C0  xor      ecx, ecx
005014C2  call     0x20e620  ; -> 0020E620 fn
005014C7  xor      ecx, ecx
005014C9  mov      dword ptr [rdi], eax
005014CB  call     0x20e620  ; -> 0020E620 fn
005014D0  mov      dword ptr [rdi + 4], eax
005014D3  xor      ecx, ecx
005014D5  mov      dword ptr [rdi + 8], ecx
005014D8  movzx    eax, word ptr [rbx]
005014DB  mov      word ptr [rdi + 0xc], ax
005014DF  movzx    eax, byte ptr [rbx + 2]
005014E3  mov      byte ptr [rdi + 0xe], al
005014E6  movzx    eax, byte ptr [rbx + 3]
005014EA  mov      byte ptr [rdi + 0xf], al
005014ED  mov      qword ptr [rdi + 0x20], rcx
005014F1  mov      qword ptr [rdi + 0x18], rcx
005014F5  mov      qword ptr [rdi + 0xb8], rcx
005014FC  mov      rcx, rdi
005014FF  mov      rbx, qword ptr [rsp + 0x30]
00501504  add      rsp, 0x20
00501508  pop      rdi
00501509  jmp      0x501440  ; -> 00501440 fn
```

## 005019D0 (104 B, extent 005019D0-00501A38)

Page context: "space, as the paired kind tables show:  | kind '+0xE' | node size (miss path) | ctor | load ('00500980' arm) | destroy ('00500850' arm) | record shape | |---|---|---|---|---|---| | '0x50' | '0x48' | '005019D0' | '00502CB0' | '00501950' (thunk '00501A40') | group/parent record: 'count16'→'+0x38', two 'count8'→'+0x3A'/'+0x3B', 'dword'→'+0x3C', then N×'0x70' records copied to '[+0x10]' and M/K child refs resolved '003AA280' as kinds '0x52'"

```
005019D0  mov      qword ptr [rsp + 8], rbx
005019D5  push     rdi
005019D6  sub      rsp, 0x20
005019DA  mov      rdi, rcx
005019DD  mov      rbx, rdx
005019E0  xor      ecx, ecx
005019E2  call     0x20e620  ; -> 0020E620 fn
005019E7  xor      ecx, ecx
005019E9  mov      dword ptr [rdi], eax
005019EB  call     0x20e620  ; -> 0020E620 fn
005019F0  mov      dword ptr [rdi + 4], eax
005019F3  xor      ecx, ecx
005019F5  mov      dword ptr [rdi + 8], ecx
005019F8  movzx    eax, word ptr [rbx]
005019FB  mov      word ptr [rdi + 0xc], ax
005019FF  movzx    eax, byte ptr [rbx + 2]
00501A03  mov      byte ptr [rdi + 0xe], al
00501A06  movzx    eax, byte ptr [rbx + 3]
00501A0A  mov      byte ptr [rdi + 0xf], al
00501A0D  and      word ptr [rdi + 0x40], 0xfffe
00501A12  mov      qword ptr [rdi + 0x10], rcx
00501A16  mov      qword ptr [rdi + 0x18], rcx
00501A1A  mov      qword ptr [rdi + 0x28], rcx
00501A1E  mov      qword ptr [rdi + 0x20], rcx
00501A22  mov      qword ptr [rdi + 0x30], rcx
00501A26  mov      rcx, rdi
00501A29  mov      rbx, qword ptr [rsp + 0x30]
00501A2E  add      rsp, 0x20
00501A32  pop      rdi
00501A33  jmp      0x501950  ; -> 00501950 fn
```

## 00503830 (78 B, extent 00503830-0050387E)

Page context: "en N×'0x70' records copied to '[+0x10]' and M/K child refs resolved '003AA280' as kinds '0x52'/'0x53' into '[+0x28]'/'[+0x30]' ('00502CCA'–'00502E7C') | | '0x51' | '0x1C' | '00503790' | '00503880' | '00503830' | two base-relative object refs at '[+0x18]' — resolve-and-free the old referents ('0020E600'×2 + '003697F0', '005038A9'–'005038C3'), then '0036A100' + '00861EBA' load of the new ones; flag '+0x16 bit 0' gates the free | | '0x52' "

```
00503830  push     rbx
00503832  sub      rsp, 0x20
00503836  test     byte ptr [rcx + 0x16], 1
0050383A  mov      rbx, rcx
0050383D  jne      0x50385c  ; -> 0050385C
0050383F  mov      ecx, dword ptr [rcx + 0x18]
00503842  call     0x20e600  ; -> 0020E600 fn
00503847  test     rax, rax
0050384A  je       0x50385c  ; -> 0050385C
0050384C  mov      ecx, dword ptr [rbx + 0x18]
0050384F  call     0x20e600  ; -> 0020E600 fn
00503854  mov      rcx, rax
00503857  call     0x3697f0  ; -> 003697F0 fn
0050385C  xor      ecx, ecx
0050385E  call     0x20e620  ; -> 0020E620 fn
00503863  mov      dword ptr [rbx + 0x18], eax
00503866  xor      eax, eax
00503868  mov      dword ptr [rbx + 0x10], eax
0050386B  mov      word ptr [rbx + 0x14], ax
0050386F  mov      eax, 0xfffe
00503874  and      word ptr [rbx + 0x16], ax
00503878  add      rsp, 0x20
0050387C  pop      rbx
0050387D  ret      
```

## 00503C50 (79 B, extent 00503C50-00503C9F)

Page context: "0', '003A22A0', '003A1DB0' | | '0x54' | '0x190' | '004354E0' | '00436D00' | '004352C0' (thunk '004355C0') | the mesh record — §22.2 of the residual page walks it field by field | | '0x55' | '0x20' | '00503C50' | '00503CD0' | '00503CA0' | counted fixed-size array: 'count16'→'+0x10', '0036A100(count·48)' → '[+0x18]', '00861EBA' from 'stream+4' ('00503CFC'–'00503D27') | | '0x56' | '0x20' | '00503D50' | '00503E30' | '00503DE0' | pointer-car"

```
00503C50  mov      qword ptr [rsp + 8], rbx
00503C55  push     rdi
00503C56  sub      rsp, 0x20
00503C5A  mov      rdi, rcx
00503C5D  mov      rbx, rdx
00503C60  xor      ecx, ecx
00503C62  call     0x20e620  ; -> 0020E620 fn
00503C67  xor      ecx, ecx
00503C69  mov      dword ptr [rdi], eax
00503C6B  call     0x20e620  ; -> 0020E620 fn
00503C70  mov      dword ptr [rdi + 4], eax
00503C73  xor      ecx, ecx
00503C75  mov      dword ptr [rdi + 8], ecx
00503C78  movzx    eax, word ptr [rbx]
00503C7B  mov      word ptr [rdi + 0xc], ax
00503C7F  movzx    eax, byte ptr [rbx + 2]
00503C83  mov      byte ptr [rdi + 0xe], al
00503C86  movzx    eax, byte ptr [rbx + 3]
00503C8A  mov      rbx, qword ptr [rsp + 0x30]
00503C8F  mov      byte ptr [rdi + 0xf], al
00503C92  mov      qword ptr [rdi + 0x18], rcx
00503C96  mov      dword ptr [rdi + 0x10], ecx
00503C99  add      rsp, 0x20
00503C9D  pop      rdi
00503C9E  ret      
```

## 00503DE0 (71 B, extent 00503DE0-00503E27)

Page context: "3CD0' | '00503CA0' | counted fixed-size array: 'count16'→'+0x10', '0036A100(count·48)' → '[+0x18]', '00861EBA' from 'stream+4' ('00503CFC'–'00503D27') | | '0x56' | '0x20' | '00503D50' | '00503E30' | '00503DE0' | pointer-carrying record, '00503880''s shape — resolve/free old referents, then resolve-store + alloc + '00861EBA' the new ('00503E49'–'00503F30') | | '0x57' | '0x30' | '00503F50' | '00504060' | '00504000' | same shape as '0x56' "

```
00503DE0  push     rbx
00503DE2  sub      rsp, 0x20
00503DE6  test     byte ptr [rcx + 0x18], 1
00503DEA  mov      rbx, rcx
00503DED  jne      0x503e0c  ; -> 00503E0C
00503DEF  mov      ecx, dword ptr [rcx + 0x10]
00503DF2  call     0x20e600  ; -> 0020E600 fn
00503DF7  test     rax, rax
00503DFA  je       0x503e0c  ; -> 00503E0C
00503DFC  mov      ecx, dword ptr [rbx + 0x10]
00503DFF  call     0x20e600  ; -> 0020E600 fn
00503E04  mov      rcx, rax
00503E07  call     0x3697f0  ; -> 003697F0 fn
00503E0C  xor      ecx, ecx
00503E0E  call     0x20e620  ; -> 0020E620 fn
00503E13  and      byte ptr [rbx + 0x18], 0xfe
00503E17  mov      dword ptr [rbx + 0x10], eax
00503E1A  mov      dword ptr [rbx + 0x14], 0
00503E21  add      rsp, 0x20
00503E25  pop      rbx
00503E26  ret      
```

## 00504000 (93 B, extent 00504000-0050405D)

Page context: "0' | pointer-carrying record, '00503880''s shape — resolve/free old referents, then resolve-store + alloc + '00861EBA' the new ('00503E49'–'00503F30') | | '0x57' | '0x30' | '00503F50' | '00504060' | '00504000' | same shape as '0x56' plus '003D7F30'/'003D7CE0' resource lookups around the copy ('00504078'–'0050412E') | | '0x58' | '0x20' | '00504170' | '00504230' | '005041F0' | single blob: 'dword count'→'+0x10', 'dword bytes'→'+0x14', buf"

```
00504000  push     rbx
00504002  sub      rsp, 0x20
00504006  mov      rbx, rcx
00504009  mov      ecx, dword ptr [rcx + 0x28]
0050400C  call     0x20e600  ; -> 0020E600 fn
00504011  test     rax, rax
00504014  je       0x504026  ; -> 00504026
00504016  mov      ecx, dword ptr [rbx + 0x28]
00504019  call     0x20e600  ; -> 0020E600 fn
0050401E  mov      rcx, rax
00504021  call     0x3697f0  ; -> 003697F0 fn
00504026  xor      ecx, ecx
00504028  call     0x20e620  ; -> 0020E620 fn
0050402D  mov      edx, dword ptr [rbx + 0x14]
00504030  mov      dword ptr [rbx + 0x28], eax
00504033  test     edx, edx
00504035  je       0x504051  ; -> 00504051
00504037  movzx    r8d, byte ptr [rbx + 0x18]
0050403C  mov      ecx, r8d
0050403F  sub      ecx, 1
00504042  je       0x504049  ; -> 00504049
00504044  cmp      ecx, 2
00504047  jne      0x504051  ; -> 00504051
00504049  mov      ecx, r8d
0050404C  call     0x3d7f30  ; -> 003D7F30 fn
00504051  xor      eax, eax
00504053  mov      qword ptr [rbx + 0x10], rax
00504057  add      rsp, 0x20
0050405B  pop      rbx
0050405C  ret      
```

## 005041F0 (50 B, extent 005041F0-00504222)

Page context: "x30' | '00503F50' | '00504060' | '00504000' | same shape as '0x56' plus '003D7F30'/'003D7CE0' resource lookups around the copy ('00504078'–'0050412E') | | '0x58' | '0x20' | '00504170' | '00504230' | '005041F0' | single blob: 'dword count'→'+0x10', 'dword bytes'→'+0x14', buffer '0020E620(0036A100(size))' → '[+0x18]', '00861EBA' from 'stream+0x10' ('00504245'–'005042A2') | | '0x59' | '0x30' | '005042C0' | '00504350' | '00504320' | string/"

```
005041F0  push     rbx
005041F2  sub      rsp, 0x20
005041F6  mov      rbx, rcx
005041F9  mov      ecx, dword ptr [rcx + 0x18]
005041FC  call     0x20e600  ; -> 0020E600 fn
00504201  test     rax, rax
00504204  je       0x504216  ; -> 00504216
00504206  mov      ecx, dword ptr [rbx + 0x18]
00504209  call     0x20e600  ; -> 0020E600 fn
0050420E  mov      rcx, rax
00504211  call     0x3697f0  ; -> 003697F0 fn
00504216  xor      eax, eax
00504218  mov      qword ptr [rbx + 0x10], rax
0050421C  add      rsp, 0x20
00504220  pop      rbx
00504221  ret      
```

## 005042C0 (82 B, extent 005042C0-00504312)

Page context: "' | '005041F0' | single blob: 'dword count'→'+0x10', 'dword bytes'→'+0x14', buffer '0020E620(0036A100(size))' → '[+0x18]', '00861EBA' from 'stream+0x10' ('00504245'–'005042A2') | | '0x59' | '0x30' | '005042C0' | '00504350' | '00504320' | string/wstring record: '0036C1D0'/'0036C140' pool helpers around '0036A100'/'0036A190' + '00861EBA' ('00504374'–'00504432') |  **Every loader runs its kind's destroy body first** — '00502CB0' opens with"

```
005042C0  mov      qword ptr [rsp + 8], rbx
005042C5  push     rdi
005042C6  sub      rsp, 0x20
005042CA  mov      rdi, rcx
005042CD  mov      rbx, rdx
005042D0  xor      ecx, ecx
005042D2  call     0x20e620  ; -> 0020E620 fn
005042D7  xor      ecx, ecx
005042D9  mov      dword ptr [rdi], eax
005042DB  call     0x20e620  ; -> 0020E620 fn
005042E0  mov      dword ptr [rdi + 4], eax
005042E3  xor      ecx, ecx
005042E5  mov      dword ptr [rdi + 8], ecx
005042E8  movzx    eax, word ptr [rbx]
005042EB  mov      word ptr [rdi + 0xc], ax
005042EF  movzx    eax, byte ptr [rbx + 2]
005042F3  mov      byte ptr [rdi + 0xe], al
005042F6  movzx    eax, byte ptr [rbx + 3]
005042FA  mov      rbx, qword ptr [rsp + 0x30]
005042FF  mov      byte ptr [rdi + 0xf], al
00504302  mov      qword ptr [rdi + 0x28], rcx
00504306  mov      byte ptr [rdi + 0x14], cl
00504309  mov      dword ptr [rdi + 0x10], ecx
0050430C  add      rsp, 0x20
00504310  pop      rdi
00504311  ret      
```

## 00532E80 (104 B, extent 00532E80-00532EE8)

Page context: " '0x1B0' frame, 'byte[rdi]' and 'dword[rdi+0x48] >= 1' gate, 'r12 = [rdi+0x20]', and the '004309C0' x15 ladder runs '[rdi+0x44]'-keyed at '[r12+0x140]'/'+0x150'+ with '0026EE00' x11, '0042FDB0' x10, '00532E80'/'005325D0'/'00533250'/'00540F40' - the default sub-walk's work body.  Interior anchor '0052958E' (function '005294F0').  '00528150' (1716 B) is the sibling '0043ED30' arm: 'byte[rcx]' gate, 'rdi = [rcx+0x20]', '0042FDB0(rdi+0x80, "

```
00532E80  movzx    r10d, word ptr [rcx + 0xb0]
00532E88  mov      r9d, dword ptr [rdx]
00532E8B  mov      ecx, r10d
00532E8E  inc      r9d
00532E91  shl      ecx, 5
00532E94  add      r9d, ecx
00532E97  shl      r9d, 4
00532E9B  cmp      dword ptr [r8 + 0x88], 0
00532EA3  je       0x532eb2  ; -> 00532EB2
00532EA5  lea      eax, [r10 + 6]
00532EA9  lea      ecx, [rax + rax*4]
00532EAC  shl      ecx, 4
00532EAF  add      r9d, ecx
00532EB2  cmp      dword ptr [r8 + 0x8c], 0
00532EBA  je       0x532ec9  ; -> 00532EC9
00532EBC  lea      eax, [r10 + 6]
00532EC0  lea      ecx, [rax + rax*4]
00532EC3  shl      ecx, 4
00532EC6  add      r9d, ecx
00532EC9  cmp      dword ptr [r8 + 0x90], 0
00532ED1  je       0x532ee0  ; -> 00532EE0
00532ED3  lea      ecx, [r10 + 6]
00532ED7  lea      edx, [rcx + rcx*4]
00532EDA  shl      edx, 4
00532EDD  add      r9d, edx
00532EE0  shr      r9d, 4
00532EE4  mov      eax, r9d
00532EE7  ret      
```

## 00538A60 (66 B, extent 00538A60-00538AA2)

Page context: " a reading aid and is not the evidence, which is the tables. Types 1–5, for instance:  | type | step | update | walk | setup | |---|---|---|---|---| | '0x01' | '00442520' | '004424E0' | '00442550' | '00538A60' | | '0x02' | '00448DE0' | '00448D70' | '004490D0' | '00538AB0' | | '0x03' | '004427A0' | '00442760' | '004427D0' | '00538B80' | | '0x04' | '00445310' | '004452D0' | '004453D0' | '00538C80' | | '0x05' | '00449970' | '00449930' | '0"

```
00538A60  mov      qword ptr [rsp + 8], rbx
00538A65  push     rdi
00538A66  sub      rsp, 0x20
00538A6A  mov      ebx, edx
00538A6C  mov      rdi, rcx
00538A6F  call     0x500470  ; -> 00500470 fn
00538A74  lea      rcx, [rdi + 0x80]
00538A7B  mov      edx, ebx
00538A7D  call     0x42fcf0  ; -> 0042FCF0 fn
00538A82  lea      rcx, [rdi + 0xd0]
00538A89  mov      edx, ebx
00538A8B  call     0x4304f0  ; -> 004304F0 fn
00538A90  mov      rbx, qword ptr [rsp + 0x30]
00538A95  lea      rax, [rdi + 0xf0]
00538A9C  add      rsp, 0x20
00538AA0  pop      rdi
00538AA1  ret      
```

## 00540C20 (76 B, extent 00540C20-00540C6C)

Page context: " gate, 'rdi = [rcx+0x20]', '0042FDB0(rdi+0x80, [rcx+0x44])' first, a '+0x1F0' '0x80808080' sentinel routed through '0026EE00', then '005479B0'/'00547A00'/'0024E2E0', '00462260' x3, '003A3CF0' x2 and '00540C20' over a '004309C0' x4/'0026EE00' x7 ladder - the paired default-arm body.  Interior anchor '005281B9' (function '00528150').  '0045DD10' (1709 B) is a '002F4020' type arm seeding '02AE8940': 'byte[rcx]' gate, 'rsi = [rcx+0x20]', '0"

```
00540C20  movzx    r10d, word ptr [rip + 0x2a4e69e]  ; -> 02F8F2C6
00540C28  and      r9d, 0xffffff
00540C2F  mov      rax, qword ptr [rip + 0x2a4e6c2]  ; -> 02F8F2F8
00540C36  lea      r8, [r10 + r10*4]
00540C3A  inc      r10w
00540C3E  lea      r11, [rax + r8*8]
00540C42  mov      word ptr [rip + 0x2a4e67c], r10w  ; -> 02F8F2C6
00540C4A  mov      qword ptr [r11], rcx
00540C4D  mov      dword ptr [r11 + 8], r9d
00540C51  movzx    eax, byte ptr [rip + 0x25adcb8]  ; -> 02AEE910
00540C58  shl      al, 4
00540C5B  or       byte ptr [r11 + 0xb], al
00540C5F  mov      dword ptr [r11 + 0xc], edx
00540C63  mov      qword ptr [r11 + 0x10], 0
00540C6B  ret      
```

## 00543940 (87 B, extent 00543940-00543997)

Page context: "54xxxx' band.  | type code | handler | shared | the type's own pair | |---|---|---|---| | ''h'' '0x68' | '00522D80' | '00540F40' | '00541DB0', '00542100' | | ''i'' '0x69' | '00523D30' | '00540F40' | '00543940', '005439D0' | | '0xA3' | '00524A50' | '00540F40' | '00544590', '00544A50' | | '0xA6' | '00524E30' | '00540F40' | '00544CE0', '00544D30' | | ''j'' '0x6A' | '00526080' | '00540DB0' | '00545EF0', '005466E0' | | '0xA8' | '005271D0' | "

```
00543940  mov      r8d, dword ptr [rdx]
00543943  mov      r9, rcx
00543946  add      r8d, 0x78
0054394A  shl      r8d, 4
0054394E  cmp      dword ptr [rcx + 0x740], 0
00543955  lea      eax, [r8 + 0x190]
0054395C  cmove    eax, r8d
00543960  cmp      dword ptr [r9 + 0x790], 0
00543968  lea      ecx, [rax + 0x190]
0054396E  cmove    ecx, eax
00543971  cmp      dword ptr [r9 + 0x7e0], 0
00543979  lea      edx, [rcx + 0x190]
0054397F  cmove    edx, ecx
00543982  cmp      dword ptr [r9 + 0x830], 0
0054398A  lea      eax, [rdx + 0x190]
00543990  cmove    eax, edx
00543993  shr      eax, 4
00543996  ret      
```

## 005439A0 (38 B, extent 005439A0-005439C6)

Page context: "' and words '+0x870', '+0x87C'/'+0x87D'/'+0x87E' copy into the '[rdi+0x230]' block at '+0', '+0x730', '+8', '+0x744', '+0x794' (1.0f staging via 'xmm6'), '003D8E50' runs four times across the block, '005439A0'/'00524320' close it and '[rbx+0x14]' lands at '[rdi+0xAC0]' - '1' on commit, early-out on the gate.  Interior anchor '00523C39' (function '00523C30').  '00366690' (80 B) is the shared angle wrap: 'xmm0' (degrees) scales by 'pi/180"

```
005439A0  mov      eax, dword ptr [rcx]
005439A2  xorps    xmm0, xmm0
005439A5  movss    xmm1, dword ptr [rip + 0x17a81fb]  ; -> 01CEBBA8 [f32 1]
005439AD  inc      eax
005439AF  cvtsi2ss xmm0, rax
005439B4  xor      eax, eax
005439B6  mov      dword ptr [rcx + 0x14], eax
005439B9  mov      dword ptr [rcx + 4], eax
005439BC  divss    xmm1, xmm0
005439C0  movss    dword ptr [rcx + 0x18], xmm1
005439C5  ret      
```

## 00544590 (68 B, extent 00544590-005445D4)

Page context: " pair | |---|---|---|---| | ''h'' '0x68' | '00522D80' | '00540F40' | '00541DB0', '00542100' | | ''i'' '0x69' | '00523D30' | '00540F40' | '00543940', '005439D0' | | '0xA3' | '00524A50' | '00540F40' | '00544590', '00544A50' | | '0xA6' | '00524E30' | '00540F40' | '00544CE0', '00544D30' | | ''j'' '0x6A' | '00526080' | '00540DB0' | '00545EF0', '005466E0' | | '0xA8' | '005271D0' | '00540F40' | '00547350', '005473A0' | | '0xA4' | '00522300' | "

```
00544590  mov      qword ptr [rsp + 8], rbx
00544595  push     rdi
00544596  sub      rsp, 0x20
0054459A  mov      rbx, rcx
0054459D  xor      edi, edi
0054459F  mov      ecx, dword ptr [rcx + 0x64]
005445A2  call     0x20e600  ; -> 0020E600 fn
005445A7  mov      ecx, dword ptr [rbx]
005445A9  test     ecx, ecx
005445AB  je       0x5445c0  ; -> 005445C0
005445AD  dec      ecx
005445AF  mov      eax, 0xcccccccd
005445B4  mul      ecx
005445B6  mov      edi, edx
005445B8  shr      edi, 4
005445BB  inc      edi
005445BD  shl      edi, 4
005445C0  mov      rbx, qword ptr [rsp + 0x30]
005445C5  lea      eax, [rdi + 0x130]
005445CB  shr      eax, 4
005445CE  add      rsp, 0x20
005445D2  pop      rdi
005445D3  ret      
```

## 005479B0 (73 B, extent 005479B0-005479F9)

Page context: "').  '00528150' (1716 B) is the sibling '0043ED30' arm: 'byte[rcx]' gate, 'rdi = [rcx+0x20]', '0042FDB0(rdi+0x80, [rcx+0x44])' first, a '+0x1F0' '0x80808080' sentinel routed through '0026EE00', then '005479B0'/'00547A00'/'0024E2E0', '00462260' x3, '003A3CF0' x2 and '00540C20' over a '004309C0' x4/'0026EE00' x7 ladder - the paired default-arm body.  Interior anchor '005281B9' (function '00528150').  '0045DD10' (1709 B) is a '002F4020' ty"

```
005479B0  xor      eax, eax
005479B2  mov      r11d, 0xf0
005479B8  mov      r10d, eax
005479BB  add      rcx, 2
005479BF  lea      r9d, [rax + 0x40]
005479C3  lea      r8d, [rax + 4]
005479C7  cmp      word ptr [rcx], ax
005479CA  je       0x5479e1  ; -> 005479E1
005479CC  test     r10d, r10d
005479CF  mov      edx, 0x100
005479D4  mov      r10d, 1
005479DA  cmove    edx, r11d
005479DE  add      r9d, edx
005479E1  add      rcx, 0x90
005479E8  sub      r8, 1
005479EC  jne      0x5479c7  ; -> 005479C7
005479EE  test     r10d, r10d
005479F1  cmovne   eax, r9d
005479F5  shr      eax, 4
005479F8  ret      
```

## 00547D80 (77 B, extent 00547D80-00547DCD)

Page context: "cond arm.  Interior anchor '0052B10E' (function '0052B080').  '0052A360' (1330 B) is a '0043ED30' sub-walk arm: 'byte[rcx]' gate and the same '0026EE00'/'0042FDB0'/'00462260' x10 triple ladder, with '00547D80'/'005480E0'/'00540F40' as its local bodies - the third sibling of the default-arm family.  Interior anchor '0052A3E0' (function '0052A360').  '00522300' (1268 B) is a '0043ED30' sub-walk arm: 'byte[rcx]' gate, '0042FDB0' x5 and '00"

```
00547D80  mov      edx, dword ptr [rdx]
00547D82  mov      r10, rcx
00547D85  mov      r9d, dword ptr [rcx + 0x140]
00547D8C  add      edx, 0x18
00547D8F  imul     r8d, r9d, 0x27
00547D93  add      edx, r8d
00547D96  shl      edx, 4
00547D99  cmp      byte ptr [rcx + 0x78], 0
00547D9D  je       0x547da8  ; -> 00547DA8
00547D9F  lea      eax, [r9 + r9*2]
00547DA3  shl      eax, 6
00547DA6  add      edx, eax
00547DA8  cmp      byte ptr [rcx + 0x79], 0
00547DAC  je       0x547db7  ; -> 00547DB7
00547DAE  lea      ecx, [r9 + r9*2]
00547DB2  shl      ecx, 6
00547DB5  add      edx, ecx
00547DB7  cmp      byte ptr [r10 + 0x7a], 0
00547DBC  je       0x547dc7  ; -> 00547DC7
00547DBE  lea      ecx, [r9 + r9*2]
00547DC2  shl      ecx, 6
00547DC5  add      edx, ecx
00547DC7  shr      edx, 4
00547DCA  mov      eax, edx
00547DCC  ret      
```

## 0054A980 (64 B, extent 0054A980-0054A9C0)

Page context: "s a '0043ED30' sub-walk arm: 'byte[rcx]' gate, '002F1F40' prelude, '0026EE00'/'0042FDB0'/'00462260' x10 triples over the '004314E0'/'00434A70'/'00434900'/'00398030'/'0039B620'/'0039B550' ladder with '0054A980'/'0054AA90'/'00540F40' - the '00523D30' shape on the second arm.  Interior anchor '0052B10E' (function '0052B080').  '0052A360' (1330 B) is a '0043ED30' sub-walk arm: 'byte[rcx]' gate and the same '0026EE00'/'0042FDB0'/'00462260' x"

```
0054A980  mov      eax, dword ptr [rdx]
0054A982  add      eax, 0x3f
0054A985  shl      eax, 4
0054A988  cmp      byte ptr [rcx + 0x156], 0
0054A98F  lea      edx, [rax + 0xc0]
0054A995  cmove    edx, eax
0054A998  cmp      byte ptr [rcx + 0x157], 0
0054A99F  lea      r8d, [rdx + 0xc0]
0054A9A6  cmove    r8d, edx
0054A9AA  cmp      byte ptr [rcx + 0x158], 0
0054A9B1  lea      eax, [r8 + 0xc0]
0054A9B8  cmove    eax, r8d
0054A9BC  shr      eax, 4
0054A9BF  ret      
```

## 005F01B0 (111 B, extent 005F01B0-005F021F)

Page context: "erior anchor '0062C34F' (the 'slot+8' store).  ## SWE2-EC7-122 update (2026-09-21) - '00625EC0' measured  '00625EC0' (8 B) is the '[+0x48] != 0' predicate its eight callers - '005D14C0', '005DD5E0', '005F01B0', '005FE200', '00604750', '006097B0', '006515C0', '0065D310' - run before touching the slot table; two instructions, 'cmp' + 'setne'. Interior anchor '00625EC4' (the 'setne').  ## SWE2-EC7-123 update (2026-09-21) - '0061D960' measu"

```
005F01B0  test     rcx, rcx
005F01B3  je       0x5f021e  ; -> 005F021E
005F01B5  push     rdi
005F01B6  sub      rsp, 0x30
005F01BA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005F01C3  mov      qword ptr [rsp + 0x40], rbx
005F01C8  mov      qword ptr [rsp + 0x48], rsi
005F01CD  mov      rsi, rcx
005F01D0  test     edx, edx
005F01D2  je       0x5f0207  ; -> 005F0207
005F01D4  mov      rbx, rcx
005F01D7  mov      edi, edx
005F01D9  nop      dword ptr [rax]
005F01E0  mov      rcx, rbx
005F01E3  call     0x625ec0  ; -> 00625EC0 fn
005F01E8  test     al, al
005F01EA  je       0x5f01f4  ; -> 005F01F4
005F01EC  mov      rcx, rbx
005F01EF  call     0x62b7b0  ; -> 0062B7B0 fn
005F01F4  mov      rcx, rbx
005F01F7  call     0x616420  ; -> 00616420 fn
005F01FC  nop      
005F01FD  add      rbx, 0x50
005F0201  sub      rdi, 1
005F0205  jne      0x5f01e0  ; -> 005F01E0
005F0207  mov      rcx, rsi
005F020A  call     0x584730  ; -> 00584730 fn
005F020F  mov      rbx, qword ptr [rsp + 0x40]
005F0214  mov      rsi, qword ptr [rsp + 0x48]
005F0219  add      rsp, 0x30
005F021D  pop      rdi
005F021E  ret      
```
