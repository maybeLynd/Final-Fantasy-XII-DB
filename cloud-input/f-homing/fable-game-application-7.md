# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 00616520 (63 B, extent 00616520-0061655F)

Documented callee on this page: `00809054`

```
00616520  push     rbx
00616522  sub      rsp, 0x30
00616526  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0061652F  lea      rbx, [rcx + 8]
00616533  lea      rcx, [rbx + 0xc0]
0061653A  call     0x16d6a0  ; -> 0016D6A0 fn
0061653F  nop      
00616540  lea      r9, [rip - 0x4a8ea7]  ; -> 0016D6A0
00616547  mov      edx, 0x18
0061654C  lea      r8d, [rdx - 0x10]
00616550  mov      rcx, rbx
00616553  call     0x809054  ; -> 00809054 fn
00616558  nop      
00616559  add      rsp, 0x30
0061655D  pop      rbx
0061655E  ret      
```

## 00616740 (51 B, extent 00616740-00616773)

Documented callee on this page: `005DDB00`

```
00616740  push     rbx
00616742  sub      rsp, 0x30
00616746  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0061674F  mov      rbx, rcx
00616752  cmp      qword ptr [rcx + 0x28], 0
00616757  jne      0x616760  ; -> 00616760
00616759  cmp      qword ptr [rcx + 0x18], 0
0061675E  je       0x616766  ; -> 00616766
00616760  call     0x62b890  ; -> 0062B890 fn
00616765  nop      
00616766  mov      rcx, rbx
00616769  add      rsp, 0x30
0061676D  pop      rbx
0061676E  jmp      0x5ddb00  ; -> 005DDB00 fn
```

## 00616780 (62 B, extent 00616780-006167BE)

Documented callee on this page: `00809054`

```
00616780  push     rbx
00616782  sub      rsp, 0x30
00616786  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0061678F  mov      rbx, rcx
00616792  add      rcx, 0xc0
00616799  call     0x16d6a0  ; -> 0016D6A0 fn
0061679E  nop      
0061679F  lea      r9, [rip - 0x4a9106]  ; -> 0016D6A0
006167A6  mov      edx, 0x18
006167AB  lea      r8d, [rdx - 0x10]
006167AF  mov      rcx, rbx
006167B2  call     0x809054  ; -> 00809054 fn
006167B7  nop      
006167B8  add      rsp, 0x30
006167BC  pop      rbx
006167BD  ret      
```

## 00619070 (104 B, extent 00619070-006190D8)

Documented callee on this page: `00584730`

```
00619070  test     rcx, rcx
00619073  je       0x6190d7  ; -> 006190D7
00619075  push     rdi
00619076  sub      rsp, 0x30
0061907A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00619083  mov      qword ptr [rsp + 0x40], rbx
00619088  mov      qword ptr [rsp + 0x48], rsi
0061908D  mov      rsi, rcx
00619090  test     edx, edx
00619092  je       0x6190c0  ; -> 006190C0
00619094  mov      rbx, rcx
00619097  mov      edi, edx
00619099  nop      dword ptr [rax]
006190A0  mov      rcx, qword ptr [rbx]
006190A3  test     rcx, rcx
006190A6  je       0x6190b6  ; -> 006190B6
006190A8  mov      eax, ecx
006190AA  not      al
006190AC  test     al, 1
006190AE  je       0x6190b6  ; -> 006190B6
006190B0  call     0x584730  ; -> 00584730 fn
006190B5  nop      
006190B6  add      rbx, 0x20
006190BA  sub      rdi, 1
006190BE  jne      0x6190a0  ; -> 006190A0
006190C0  mov      rcx, rsi
006190C3  call     0x584730  ; -> 00584730 fn
006190C8  mov      rbx, qword ptr [rsp + 0x40]
006190CD  mov      rsi, qword ptr [rsp + 0x48]
006190D2  add      rsp, 0x30
006190D6  pop      rdi
006190D7  ret      
```

## 0061CF20 (115 B, extent 0061CF20-0061CF93)

Documented callee on this page: `0017D260`

```
0061CF20  push     rbx
0061CF22  sub      rsp, 0x20
0061CF26  mov      ebx, edx
0061CF28  lea      r8, [rcx + 8]
0061CF2C  test     edx, edx
0061CF2E  jne      0x61cf38  ; -> 0061CF38
0061CF30  xor      eax, eax
0061CF32  add      rsp, 0x20
0061CF36  pop      rbx
0061CF37  ret      
0061CF38  cmp      ebx, 1
0061CF3B  jbe      0x61cf52  ; -> 0061CF52
0061CF3D  lea      rcx, [rbx + rbx*4]
0061CF41  mov      edx, 8
0061CF46  shl      rcx, 3
0061CF4A  call     0x17d260  ; -> 0017D260 fn
0061CF4F  mov      r8, rax
0061CF52  test     r8, r8
0061CF55  je       0x61cf8a  ; -> 0061CF8A
0061CF57  test     ebx, ebx
0061CF59  je       0x61cf8a  ; -> 0061CF8A
0061CF5B  lea      rcx, [r8 + 0x10]
0061CF5F  mov      rdx, rbx
0061CF62  xor      r9d, r9d
0061CF65  lea      rax, [rcx - 0x10]
0061CF69  test     rax, rax
0061CF6C  je       0x61cf80  ; -> 0061CF80
0061CF6E  mov      qword ptr [rax], r9
0061CF71  mov      qword ptr [rcx - 8], r9
0061CF75  mov      qword ptr [rcx], r9
0061CF78  mov      qword ptr [rcx + 8], r9
0061CF7C  mov      dword ptr [rcx + 0x10], r9d
0061CF80  add      rcx, 0x28
0061CF84  sub      rdx, 1
0061CF88  jne      0x61cf65  ; -> 0061CF65
0061CF8A  mov      rax, r8
0061CF8D  add      rsp, 0x20
0061CF91  pop      rbx
0061CF92  ret      
```

## 0061D030 (203 B, extent 0061D030-0061D0FB)

Documented callee on this page: `0017D260`

```
0061D030  mov      qword ptr [rsp + 8], rbx
0061D035  mov      qword ptr [rsp + 0x10], rsi
0061D03A  push     rdi
0061D03B  sub      rsp, 0x20
0061D03F  mov      edi, r9d
0061D042  mov      rsi, r8
0061D045  mov      ebx, edx
0061D047  lea      r10, [rcx + 8]
0061D04B  test     edx, edx
0061D04D  jne      0x61d061  ; -> 0061D061
0061D04F  xor      eax, eax
0061D051  mov      rbx, qword ptr [rsp + 0x30]
0061D056  mov      rsi, qword ptr [rsp + 0x38]
0061D05B  add      rsp, 0x20
0061D05F  pop      rdi
0061D060  ret      
0061D061  cmp      ebx, 1
0061D064  jbe      0x61d07a  ; -> 0061D07A
0061D066  mov      rcx, rbx
0061D069  mov      edx, 8
0061D06E  shl      rcx, 4
0061D072  call     0x17d260  ; -> 0017D260 fn
0061D077  mov      r10, rax
0061D07A  test     r10, r10
0061D07D  je       0x61d0e8  ; -> 0061D0E8
0061D07F  mov      rdx, r10
0061D082  test     edi, edi
0061D084  je       0x61d0ba  ; -> 0061D0BA
0061D086  lea      r8, [rsi + 0xc]
0061D08A  mov      r9, rdi
0061D08D  nop      dword ptr [rax]
0061D090  mov      rcx, rdx
0061D093  add      rdx, 0x10
0061D097  test     rcx, rcx
0061D09A  je       0x61d0b4  ; -> 0061D0B4
0061D09C  mov      rax, qword ptr [r8 - 0xc]
0061D0A0  mov      qword ptr [rcx], rax
0061D0A3  mov      eax, dword ptr [r8 - 4]
0061D0A7  mov      dword ptr [rcx + 8], eax
0061D0AA  mov      eax, dword ptr [r8]
0061D0AD  add      r8, 0x10
0061D0B1  mov      dword ptr [rcx + 0xc], eax
0061D0B4  sub      r9, 1
0061D0B8  jne      0x61d090  ; -> 0061D090
0061D0BA  sub      ebx, edi
0061D0BC  je       0x61d0e8  ; -> 0061D0E8
0061D0BE  mov      rax, rdi
0061D0C1  mov      ecx, ebx
0061D0C3  shl      rax, 4
0061D0C7  add      rax, r10
0061D0CA  xor      edx, edx
0061D0CC  nop      dword ptr [rax]
0061D0D0  test     rax, rax
0061D0D3  je       0x61d0de  ; -> 0061D0DE
0061D0D5  mov      qword ptr [rax], rdx
0061D0D8  mov      dword ptr [rax + 8], edx
0061D0DB  mov      dword ptr [rax + 0xc], edx
0061D0DE  add      rax, 0x10
0061D0E2  sub      rcx, 1
0061D0E6  jne      0x61d0d0  ; -> 0061D0D0
0061D0E8  mov      rbx, qword ptr [rsp + 0x30]
0061D0ED  mov      rax, r10
0061D0F0  mov      rsi, qword ptr [rsp + 0x38]
0061D0F5  add      rsp, 0x20
0061D0F9  pop      rdi
0061D0FA  ret      
```

## 00627CF0 (175 B, extent 00627CF0-00627D9F)

Documented callee on this page: `00584730`

```
00627CF0  mov      qword ptr [rsp + 0x10], rbx
00627CF5  mov      qword ptr [rsp + 0x18], rbp
00627CFA  mov      qword ptr [rsp + 0x20], rsi
00627CFF  push     rdi
00627D00  sub      rsp, 0x20
00627D04  mov      r9d, dword ptr [rcx]
00627D07  mov      esi, edx
00627D09  btr      r9d, 0x1f
00627D0E  mov      rdi, rcx
00627D11  cmp      edx, dword ptr [rcx]
00627D13  je       0x627d88  ; -> 00627D88
00627D15  cmp      r9d, 1
00627D19  jbe      0x627d21  ; -> 00627D21
00627D1B  mov      rbx, qword ptr [rcx + 8]
00627D1F  jmp      0x627d2e  ; -> 00627D2E
00627D21  test     r9d, r9d
00627D24  je       0x627d2c  ; -> 00627D2C
00627D26  lea      rbx, [rcx + 8]
00627D2A  jmp      0x627d2e  ; -> 00627D2E
00627D2C  xor      ebx, ebx
00627D2E  cmp      esi, r9d
00627D31  mov      r8, rbx
00627D34  cmovb    r9d, esi
00627D38  call     0x61d030  ; -> 0061D030 fn
00627D3D  mov      rbp, rax
00627D40  test     rax, rax
00627D43  jne      0x627d4e  ; -> 00627D4E
00627D45  test     esi, esi
00627D47  je       0x627d4e  ; -> 00627D4E
00627D49  lea      eax, [rbp + 0xd]
00627D4C  jmp      0x627d8a  ; -> 00627D8A
00627D4E  mov      qword ptr [rsp + 0x30], r14
00627D53  lea      r14, [rdi + 8]
00627D57  cmp      rbx, rbp
00627D5A  je       0x627d79  ; -> 00627D79
00627D5C  cmp      rbx, r14
00627D5F  je       0x627d79  ; -> 00627D79
00627D61  mov      eax, dword ptr [rdi]
00627D63  shr      eax, 0x1f
00627D66  not      al
00627D68  test     al, 1
00627D6A  je       0x627d79  ; -> 00627D79
00627D6C  test     rbx, rbx
00627D6F  je       0x627d79  ; -> 00627D79
00627D71  mov      rcx, rbx
00627D74  call     0x584730  ; -> 00584730 fn
00627D79  cmp      rbp, r14
00627D7C  je       0x627d81  ; -> 00627D81
00627D7E  mov      qword ptr [r14], rbp
00627D81  mov      r14, qword ptr [rsp + 0x30]
00627D86  mov      dword ptr [rdi], esi
00627D88  xor      eax, eax
00627D8A  mov      rbx, qword ptr [rsp + 0x38]
00627D8F  mov      rbp, qword ptr [rsp + 0x40]
00627D94  mov      rsi, qword ptr [rsp + 0x48]
00627D99  add      rsp, 0x20
00627D9D  pop      rdi
00627D9E  ret      
```

## 006339A0 (55 B, extent 006339A0-006339D7)

Documented callee on this page: `00809950`

```
006339A0  push     rbx
006339A2  sub      rsp, 0x20
006339A6  lea      rax, [rip + 0x7246eb]  ; -> 00D58098
006339AD  mov      rbx, rcx
006339B0  mov      qword ptr [rcx], rax
006339B3  mov      rax, qword ptr [rcx + 8]
006339B7  mov      qword ptr [rax + 0x50], 0
006339BF  test     dl, 1
006339C2  je       0x6339ce  ; -> 006339CE
006339C4  mov      edx, 0x20
006339C9  call     0x809950  ; -> 00809950 fn
006339CE  mov      rax, rbx
006339D1  add      rsp, 0x20
006339D5  pop      rbx
006339D6  ret      
```

## 00664F10 (110 B, extent 00664F10-00664F7E)

Documented callee on this page: `0017D260`

```
00664F10  mov      qword ptr [rsp + 0x10], rbx
00664F15  push     rsi
00664F16  sub      rsp, 0x20
00664F1A  mov      esi, ecx
00664F1C  mov      rbx, rdx
00664F1F  test     ecx, ecx
00664F21  je       0x664f71  ; -> 00664F71
00664F23  mov      qword ptr [rsp + 0x30], rdi
00664F28  mov      edx, 4
00664F2D  mov      ecx, esi
00664F2F  mov      edi, esi
00664F31  call     0x17d260  ; -> 0017D260 fn
00664F36  mov      r8, rax
00664F39  test     rax, rax
00664F3C  je       0x664f61  ; -> 00664F61
00664F3E  mov      rcx, rax
00664F41  test     esi, esi
00664F43  je       0x664f61  ; -> 00664F61
00664F45  mov      rdx, rcx
00664F48  inc      rcx
00664F4B  test     rdx, rdx
00664F4E  je       0x664f58  ; -> 00664F58
00664F50  movzx    eax, byte ptr [rbx]
00664F53  inc      rbx
00664F56  mov      byte ptr [rdx], al
00664F58  sub      rdi, 1
00664F5C  jne      0x664f45  ; -> 00664F45
00664F5E  mov      rax, r8
00664F61  mov      rdi, qword ptr [rsp + 0x30]
00664F66  mov      rbx, qword ptr [rsp + 0x38]
00664F6B  add      rsp, 0x20
00664F6F  pop      rsi
00664F70  ret      
00664F71  xor      eax, eax
00664F73  mov      rbx, qword ptr [rsp + 0x38]
00664F78  add      rsp, 0x20
00664F7C  pop      rsi
00664F7D  ret      
```

## 00665550 (205 B, extent 00665550-0066561D)

Documented callee on this page: `0017D260`

```
00665550  mov      qword ptr [rsp + 8], rbx
00665555  mov      qword ptr [rsp + 0x10], rbp
0066555A  mov      qword ptr [rsp + 0x18], rsi
0066555F  push     rdi
00665560  sub      rsp, 0x20
00665564  xor      ebp, ebp
00665566  mov      edi, r8d
00665569  mov      ebx, ecx
0066556B  mov      rsi, rdx
0066556E  test     ecx, ecx
00665570  je       0x665605  ; -> 00665605
00665576  lea      rcx, [rbx + rbx*2]
0066557A  shl      rcx, 3
0066557E  lea      edx, [rbp + 8]
00665581  call     0x17d260  ; -> 0017D260 fn
00665586  mov      r10, rax
00665589  test     rax, rax
0066558C  je       0x665608  ; -> 00665608
0066558E  mov      r8, rax
00665591  test     edi, edi
00665593  je       0x6655d0  ; -> 006655D0
00665595  lea      rdx, [rsi + 0x10]
00665599  mov      r9d, edi
0066559C  nop      dword ptr [rax]
006655A0  mov      rcx, r8
006655A3  add      r8, 0x18
006655A7  test     rcx, rcx
006655AA  je       0x6655ca  ; -> 006655CA
006655AC  mov      eax, dword ptr [rdx - 0x10]
006655AF  mov      dword ptr [rcx], eax
006655B1  mov      rax, qword ptr [rdx - 8]
006655B5  mov      qword ptr [rcx + 8], rax
006655B9  movzx    eax, byte ptr [rdx]
006655BC  mov      byte ptr [rcx + 0x10], al
006655BF  movzx    eax, byte ptr [rdx + 1]
006655C3  add      rdx, 0x18
006655C7  mov      byte ptr [rcx + 0x11], al
006655CA  sub      r9, 1
006655CE  jne      0x6655a0  ; -> 006655A0
006655D0  sub      ebx, edi
006655D2  je       0x665600  ; -> 00665600
006655D4  lea      rax, [rdi + 1]
006655D8  mov      edx, ebx
006655DA  lea      rax, [rdi + rax*2]
006655DE  lea      rax, [r10 + rax*8]
006655E2  lea      rcx, [rax - 0x10]
006655E6  test     rcx, rcx
006655E9  je       0x6655f6  ; -> 006655F6
006655EB  mov      dword ptr [rcx], ebp
006655ED  mov      qword ptr [rax - 8], rbp
006655F1  mov      word ptr [rax], 0xff34
006655F6  add      rax, 0x18
006655FA  sub      rdx, 1
006655FE  jne      0x6655e2  ; -> 006655E2
00665600  mov      rax, r10
00665603  jmp      0x665608  ; -> 00665608
00665605  mov      rax, rbp
00665608  mov      rbx, qword ptr [rsp + 0x30]
0066560D  mov      rbp, qword ptr [rsp + 0x38]
00665612  mov      rsi, qword ptr [rsp + 0x40]
00665617  add      rsp, 0x20
0066561B  pop      rdi
0066561C  ret      
```

## 0066F5F0 (130 B, extent 0066F5F0-0066F672)

Documented callee on this page: `0017D260`

```
0066F5F0  push     rbx
0066F5F2  sub      rsp, 0x20
0066F5F6  mov      ebx, edx
0066F5F8  lea      r8, [rcx + 8]
0066F5FC  test     edx, edx
0066F5FE  jne      0x66f608  ; -> 0066F608
0066F600  xor      eax, eax
0066F602  add      rsp, 0x20
0066F606  pop      rbx
0066F607  ret      
0066F608  cmp      ebx, 1
0066F60B  jbe      0x66f622  ; -> 0066F622
0066F60D  lea      rcx, [rbx + rbx*8]
0066F611  mov      edx, 8
0066F616  shl      rcx, 3
0066F61A  call     0x17d260  ; -> 0017D260 fn
0066F61F  mov      r8, rax
0066F622  test     r8, r8
0066F625  je       0x66f669  ; -> 0066F669
0066F627  test     ebx, ebx
0066F629  je       0x66f669  ; -> 0066F669
0066F62B  lea      rcx, [r8 + 0x10]
0066F62F  mov      rdx, rbx
0066F632  xor      r9d, r9d
0066F635  lea      r10, [rip + 0x6f9794]  ; -> 00D68DD0
0066F63C  nop      dword ptr [rax]
0066F640  lea      rax, [rcx - 0x10]
0066F644  test     rax, rax
0066F647  je       0x66f65f  ; -> 0066F65F
0066F649  mov      qword ptr [rax], r9
0066F64C  mov      qword ptr [rcx - 8], r9
0066F650  mov      qword ptr [rcx], r9
0066F653  mov      qword ptr [rcx + 8], r9
0066F657  mov      dword ptr [rcx + 0x10], r9d
0066F65B  mov      qword ptr [rcx + 0x18], r10
0066F65F  add      rcx, 0x48
0066F663  sub      rdx, 1
0066F667  jne      0x66f640  ; -> 0066F640
0066F669  mov      rax, r8
0066F66C  add      rsp, 0x20
0066F670  pop      rbx
0066F671  ret      
```

## 0066F680 (130 B, extent 0066F680-0066F702)

Documented callee on this page: `0017D260`

```
0066F680  push     rbx
0066F682  sub      rsp, 0x20
0066F686  mov      ebx, edx
0066F688  lea      r8, [rcx + 8]
0066F68C  test     edx, edx
0066F68E  jne      0x66f698  ; -> 0066F698
0066F690  xor      eax, eax
0066F692  add      rsp, 0x20
0066F696  pop      rbx
0066F697  ret      
0066F698  cmp      ebx, 1
0066F69B  jbe      0x66f6b2  ; -> 0066F6B2
0066F69D  lea      rcx, [rbx + rbx*8]
0066F6A1  mov      edx, 8
0066F6A6  shl      rcx, 3
0066F6AA  call     0x17d260  ; -> 0017D260 fn
0066F6AF  mov      r8, rax
0066F6B2  test     r8, r8
0066F6B5  je       0x66f6f9  ; -> 0066F6F9
0066F6B7  test     ebx, ebx
0066F6B9  je       0x66f6f9  ; -> 0066F6F9
0066F6BB  lea      rcx, [r8 + 0x10]
0066F6BF  mov      rdx, rbx
0066F6C2  xor      r9d, r9d
0066F6C5  lea      r10, [rip + 0x6f9714]  ; -> 00D68DE0
0066F6CC  nop      dword ptr [rax]
0066F6D0  lea      rax, [rcx - 0x10]
0066F6D4  test     rax, rax
0066F6D7  je       0x66f6ef  ; -> 0066F6EF
0066F6D9  mov      qword ptr [rax], r9
0066F6DC  mov      qword ptr [rcx - 8], r9
0066F6E0  mov      qword ptr [rcx], r9
0066F6E3  mov      qword ptr [rcx + 8], r9
0066F6E7  mov      dword ptr [rcx + 0x10], r9d
0066F6EB  mov      qword ptr [rcx + 0x18], r10
0066F6EF  add      rcx, 0x48
0066F6F3  sub      rdx, 1
0066F6F7  jne      0x66f6d0  ; -> 0066F6D0
0066F6F9  mov      rax, r8
0066F6FC  add      rsp, 0x20
0066F700  pop      rbx
0066F701  ret      
```

## 00671E80 (342 B, extent 00671E80-00671FD6)

Documented callee on this page: `00808F10`

```
00671E80  push     rbp
00671E82  push     r12
00671E84  push     r13
00671E86  push     r14
00671E88  push     r15
00671E8A  sub      rsp, 0x40
00671E8E  lea      rbp, [rsp + 0x30]
00671E93  mov      qword ptr [rbp + 0x40], rbx
00671E97  mov      qword ptr [rbp + 0x48], rsi
00671E9B  mov      qword ptr [rbp + 0x50], rdi
00671E9F  mov      rax, qword ptr [rip + 0x18d298a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00671EA6  xor      rax, rbp
00671EA9  mov      qword ptr [rbp], rax
00671EAD  mov      r15, qword ptr [rbp + 0x60]
00671EB1  xor      ebx, ebx
00671EB3  mov      rsi, qword ptr [rbp + 0x78]
00671EB7  mov      r12, r9
00671EBA  mov      r13, qword ptr [rbp + 0x80]
00671EC1  mov      rax, rdx
00671EC4  mov      qword ptr [r9], rbx
00671EC7  mov      r14, rcx
00671ECA  mov      dword ptr [r15], ebx
00671ECD  mov      edi, dword ptr [rsi]
00671ECF  and      edi, 0x7fffffff
00671ED5  jbe      0x671ef5  ; -> 00671EF5
00671ED7  mov      r8, qword ptr [rsi + 8]
00671EDB  mov      r9d, edi
00671EDE  xor      edx, edx
00671EE0  mov      qword ptr [rsp + 0x20], r13
00671EE5  mov      rcx, rax
00671EE8  call     0x61c920  ; -> 0061C920 fn
00671EED  test     eax, eax
00671EEF  jne      0x671fb0  ; -> 00671FB0
00671EF5  mov      eax, edi
00671EF7  shl      rax, 3
00671EFB  lea      rcx, [rax + 0xf]
00671EFF  cmp      rcx, rax
00671F02  ja       0x671f0e  ; -> 00671F0E
00671F04  movabs   rcx, 0xffffffffffffff0
00671F0E  and      rcx, 0xfffffffffffffff0
00671F12  mov      rax, rcx
00671F15  call     0x808f10  ; -> 00808F10 fn
00671F1A  mov      r10d, dword ptr [rbp + 0x68]
00671F1E  sub      rsp, rcx
00671F21  lea      r11, [rsp + 0x30]
00671F26  test     edi, edi
00671F28  je       0x671f87  ; -> 00671F87
00671F2A  mov      rdx, qword ptr [rsi + 8]
00671F2E  xor      r9d, r9d
00671F31  test     edi, edi
00671F33  je       0x671f87  ; -> 00671F87
00671F35  mov      r8, r11
00671F38  cmp      dword ptr [rdx + 0x78], 0
00671F3C  je       0x671f6d  ; -> 00671F6D
00671F3E  mov      qword ptr [r8], rdx
00671F41  test     rbx, rbx
00671F44  jne      0x671f74  ; -> 00671F74
00671F46  mov      rax, qword ptr [r14 + 0x28]
00671F4A  mov      rcx, r10
00671F4D  add      rcx, rcx
00671F50  mov      ecx, dword ptr [rax + rcx*8]
00671F53  mov      rax, qword ptr [r14 + 0x18]
00671F57  add      ecx, r9d
00671F5A  lea      rcx, [rcx + rcx*2]
00671F5E  mov      rcx, qword ptr [rax + rcx*8 + 8]
00671F63  cmp      byte ptr [rcx + 0x10], bl
00671F66  je       0x671f74  ; -> 00671F74
00671F68  mov      rbx, rdx
00671F6B  jmp      0x671f74  ; -> 00671F74
00671F6D  mov      qword ptr [r8], 0
00671F74  inc      r9d
00671F77  add      r8, 8
00671F7B  add      rdx, 0x88
00671F82  cmp      r9d, edi
00671F85  jb       0x671f38  ; -> 00671F38
00671F87  mov      rax, qword ptr [r14]
00671F8A  mov      r9, r11
00671F8D  mov      r8, qword ptr [rbp + 0x70]
00671F91  mov      edx, r10d
00671F94  mov      rcx, r14
00671F97  mov      qword ptr [rsp + 0x20], r13
00671F9C  call     qword ptr [rax + 0x28]
00671F9F  mov      qword ptr [r12], rax
00671FA3  test     rbx, rbx
00671FA6  je       0x671fae  ; -> 00671FAE
00671FA8  mov      eax, dword ptr [rbx + 4]
00671FAB  mov      dword ptr [r15], eax
00671FAE  xor      eax, eax
00671FB0  mov      rcx, qword ptr [rbp]
00671FB4  xor      rcx, rbp
00671FB7  call     0x808c40  ; -> 00808C40 fn
00671FBC  mov      rbx, qword ptr [rbp + 0x40]
00671FC0  mov      rsi, qword ptr [rbp + 0x48]
00671FC4  mov      rdi, qword ptr [rbp + 0x50]
00671FC8  lea      rsp, [rbp + 0x10]
00671FCC  pop      r15
00671FCE  pop      r14
00671FD0  pop      r13
00671FD2  pop      r12
00671FD4  pop      rbp
00671FD5  ret      
```

## 00673030 (243 B, extent 00673030-00673123)

Documented callee on this page: `00584730`

```
00673030  mov      qword ptr [rsp + 0x18], rbx
00673035  push     rdi
00673036  sub      rsp, 0x20
0067303A  mov      rdi, rdx
0067303D  mov      rbx, rcx
00673040  test     r8d, r8d
00673043  jns      0x673055  ; -> 00673055
00673045  mov      eax, 5
0067304A  mov      rbx, qword ptr [rsp + 0x40]
0067304F  add      rsp, 0x20
00673053  pop      rdi
00673054  ret      
00673055  mov      eax, dword ptr [rcx]
00673057  btr      eax, 0x1f
0067305B  mov      qword ptr [rsp + 0x30], rsi
00673060  mov      qword ptr [rsp + 0x38], r14
00673065  cmp      eax, 1
00673068  jbe      0x673070  ; -> 00673070
0067306A  mov      rcx, qword ptr [rcx + 8]
0067306E  jmp      0x67307c  ; -> 0067307C
00673070  test     eax, eax
00673072  je       0x67307a  ; -> 0067307A
00673074  add      rcx, 8
00673078  jmp      0x67307c  ; -> 0067307C
0067307A  xor      ecx, ecx
0067307C  mov      esi, r8d
0067307F  bts      esi, 0x1f
00673083  cmp      r8d, 1
00673087  jne      0x6730df  ; -> 006730DF
00673089  lea      rdx, [rbx + 8]
0067308D  test     rdx, rdx
00673090  je       0x6730d7  ; -> 006730D7
00673092  mov      rax, qword ptr [rdi]
00673095  mov      qword ptr [rdx], rax
00673098  mov      rax, qword ptr [rdi + 8]
0067309C  mov      qword ptr [rdx + 8], rax
006730A0  mov      rax, qword ptr [rdi + 0x10]
006730A4  mov      qword ptr [rdx + 0x10], rax
006730A8  mov      rax, qword ptr [rdi + 0x18]
006730AC  mov      qword ptr [rdx + 0x18], rax
006730B0  mov      eax, dword ptr [rdi + 0x20]
006730B3  mov      dword ptr [rdx + 0x20], eax
006730B6  lea      rax, [rip + 0x6f5d23]  ; -> 00D68DE0
006730BD  mov      qword ptr [rdx + 0x28], rax
006730C1  mov      rax, qword ptr [rdi + 0x30]
006730C5  mov      qword ptr [rdx + 0x30], rax
006730C9  mov      eax, dword ptr [rdi + 0x38]
006730CC  mov      dword ptr [rdx + 0x38], eax
006730CF  mov      rax, qword ptr [rdi + 0x40]
006730D3  mov      qword ptr [rdx + 0x40], rax
006730D7  mov      rdi, rdx
006730DA  mov      esi, 1
006730DF  lea      r14, [rbx + 8]
006730E3  cmp      rcx, rdi
006730E6  je       0x673102  ; -> 00673102
006730E8  cmp      rcx, r14
006730EB  je       0x673102  ; -> 00673102
006730ED  mov      eax, dword ptr [rbx]
006730EF  shr      eax, 0x1f
006730F2  not      al
006730F4  test     al, 1
006730F6  je       0x673102  ; -> 00673102
006730F8  test     rcx, rcx
006730FB  je       0x673102  ; -> 00673102
006730FD  call     0x584730  ; -> 00584730 fn
00673102  cmp      rdi, r14
00673105  je       0x67310a  ; -> 0067310A
00673107  mov      qword ptr [r14], rdi
0067310A  mov      r14, qword ptr [rsp + 0x38]
0067310F  xor      eax, eax
00673111  mov      dword ptr [rbx], esi
00673113  mov      rsi, qword ptr [rsp + 0x30]
00673118  mov      rbx, qword ptr [rsp + 0x40]
0067311D  add      rsp, 0x20
00673121  pop      rdi
00673122  ret      
```

## 00675700 (62 B, extent 00675700-0067573E)

Documented callee on this page: `00809950`

```
00675700  mov      qword ptr [rsp + 8], rbx
00675705  push     rdi
00675706  sub      rsp, 0x20
0067570A  lea      rax, [rip + 0x6f6c67]  ; -> 00D6C378
00675711  mov      ebx, edx
00675713  mov      qword ptr [rcx], rax
00675716  mov      rdi, rcx
00675719  call     0x633770  ; -> 00633770 fn
0067571E  test     bl, 1
00675721  je       0x675730  ; -> 00675730
00675723  mov      edx, 0x20
00675728  mov      rcx, rdi
0067572B  call     0x809950  ; -> 00809950 fn
00675730  mov      rax, rdi
00675733  mov      rbx, qword ptr [rsp + 0x30]
00675738  add      rsp, 0x20
0067573C  pop      rdi
0067573D  ret      
```

## 0067B470 (80 B, extent 0067B470-0067B4C0)

Documented callee on this page: `00584730`

```
0067B470  push     rbx
0067B472  sub      rsp, 0x30
0067B476  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0067B47F  mov      rbx, rcx
0067B482  add      rcx, 0x40
0067B486  call     0x663170  ; -> 00663170 fn
0067B48B  nop      
0067B48C  lea      rcx, [rbx + 0x30]
0067B490  call     0x1b6ef0  ; -> 001B6EF0 fn
0067B495  nop      
0067B496  mov      eax, dword ptr [rbx + 8]
0067B499  shr      eax, 0x1f
0067B49C  not      al
0067B49E  test     al, 1
0067B4A0  je       0x67b4b1  ; -> 0067B4B1
0067B4A2  mov      rcx, qword ptr [rbx + 0x10]
0067B4A6  test     rcx, rcx
0067B4A9  je       0x67b4b1  ; -> 0067B4B1
0067B4AB  call     0x584730  ; -> 00584730 fn
0067B4B0  nop      
0067B4B1  xor      eax, eax
0067B4B3  mov      qword ptr [rbx + 0x10], rax
0067B4B7  mov      dword ptr [rbx + 8], eax
0067B4BA  add      rsp, 0x30
0067B4BE  pop      rbx
0067B4BF  ret      
```

## 00687F30 (61 B, extent 00687F30-00687F6D)

Documented callee on this page: `00584730`

```
00687F30  push     rbx
00687F32  sub      rsp, 0x30
00687F36  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00687F3F  mov      rbx, rdx
00687F42  mov      rcx, rdx
00687F45  call     0x6a27c0  ; -> 006A27C0 fn
00687F4A  nop      
00687F4B  mov      rcx, qword ptr [rbx + 0x118]
00687F52  test     rcx, rcx
00687F55  je       0x687f65  ; -> 00687F65
00687F57  mov      eax, ecx
00687F59  not      al
00687F5B  test     al, 1
00687F5D  je       0x687f65  ; -> 00687F65
00687F5F  call     0x584730  ; -> 00584730 fn
00687F64  nop      
00687F65  mov      al, 1
00687F67  add      rsp, 0x30
00687F6B  pop      rbx
00687F6C  ret      
```

## 006890D0 (79 B, extent 006890D0-0068911F)

Documented callee on this page: `00584730`

```
006890D0  push     rbx
006890D2  sub      rsp, 0x30
006890D6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006890DF  mov      rbx, rdx
006890E2  mov      rcx, qword ptr [rdx + 0xd8]
006890E9  test     rcx, rcx
006890EC  je       0x6890f4  ; -> 006890F4
006890EE  call     0x6a4670  ; -> 006A4670 fn
006890F3  nop      
006890F4  mov      rcx, rbx
006890F7  call     0x6a27c0  ; -> 006A27C0 fn
006890FC  nop      
006890FD  mov      rcx, qword ptr [rbx + 0x118]
00689104  test     rcx, rcx
00689107  je       0x689117  ; -> 00689117
00689109  mov      eax, ecx
0068910B  not      al
0068910D  test     al, 1
0068910F  je       0x689117  ; -> 00689117
00689111  call     0x584730  ; -> 00584730 fn
00689116  nop      
00689117  mov      al, 1
00689119  add      rsp, 0x30
0068911D  pop      rbx
0068911E  ret      
```

## 00691A60 (69 B, extent 00691A60-00691AA5)

Documented callee on this page: `00584730`

```
00691A60  push     rbx
00691A62  sub      rsp, 0x30
00691A66  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00691A6F  mov      rbx, rcx
00691A72  mov      ecx, dword ptr [rcx]
00691A74  mov      eax, ecx
00691A76  shr      eax, 0x1f
00691A79  not      al
00691A7B  test     al, 1
00691A7D  je       0x691a97  ; -> 00691A97
00691A7F  btr      ecx, 0x1f
00691A83  cmp      ecx, 1
00691A86  jbe      0x691a97  ; -> 00691A97
00691A88  mov      rcx, qword ptr [rbx + 8]
00691A8C  test     rcx, rcx
00691A8F  je       0x691a97  ; -> 00691A97
00691A91  call     0x584730  ; -> 00584730 fn
00691A96  nop      
00691A97  xor      eax, eax
00691A99  mov      dword ptr [rbx], eax
00691A9B  mov      qword ptr [rbx + 8], rax
00691A9F  add      rsp, 0x30
00691AA3  pop      rbx
00691AA4  ret      
```

## 00693C40 (140 B, extent 00693C40-00693CCC)

Documented callee on this page: `0017D260`

```
00693C40  mov      qword ptr [rsp + 0x10], rsi
00693C45  push     rdi
00693C46  sub      rsp, 0x20
00693C4A  mov      esi, ecx
00693C4C  mov      rdi, rdx
00693C4F  test     ecx, ecx
00693C51  je       0x693cbf  ; -> 00693CBF
00693C53  lea      rcx, [rsi + rsi*2]
00693C57  mov      qword ptr [rsp + 0x30], rbx
00693C5C  shl      rcx, 4
00693C60  mov      edx, 8
00693C65  mov      ebx, esi
00693C67  call     0x17d260  ; -> 0017D260 fn
00693C6C  mov      rdx, rax
00693C6F  test     rax, rax
00693C72  je       0x693caf  ; -> 00693CAF
00693C74  mov      rcx, rax
00693C77  test     esi, esi
00693C79  je       0x693caf  ; -> 00693CAF
00693C7B  nop      dword ptr [rax + rax]
00693C80  mov      rax, rcx
00693C83  add      rcx, 0x30
00693C87  test     rax, rax
00693C8A  je       0x693ca6  ; -> 00693CA6
00693C8C  movups   xmm0, xmmword ptr [rdi]
00693C8F  movups   xmmword ptr [rax], xmm0
00693C92  movups   xmm1, xmmword ptr [rdi + 0x10]
00693C96  movups   xmmword ptr [rax + 0x10], xmm1
00693C9A  movups   xmm0, xmmword ptr [rdi + 0x20]
00693C9E  add      rdi, 0x30
00693CA2  movups   xmmword ptr [rax + 0x20], xmm0
00693CA6  sub      rbx, 1
00693CAA  jne      0x693c80  ; -> 00693C80
00693CAC  mov      rax, rdx
00693CAF  mov      rbx, qword ptr [rsp + 0x30]
00693CB4  mov      rsi, qword ptr [rsp + 0x38]
00693CB9  add      rsp, 0x20
00693CBD  pop      rdi
00693CBE  ret      
00693CBF  xor      eax, eax
00693CC1  mov      rsi, qword ptr [rsp + 0x38]
00693CC6  add      rsp, 0x20
00693CCA  pop      rdi
00693CCB  ret      
```
