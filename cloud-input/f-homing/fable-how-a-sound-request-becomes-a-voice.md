# F homing pack (FABLE): `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 19. No bearing page cites them and no documented function calls them directly.

## 001DBFA0 (84 B, extent 001DBFA0-001DBFF4)

Documented callee on this page: `00210B30`

```
001DBFA0  mov      qword ptr [rsp + 8], rbx
001DBFA5  mov      qword ptr [rsp + 0x10], rbp
001DBFAA  mov      qword ptr [rsp + 0x18], rsi
001DBFAF  push     rdi
001DBFB0  sub      rsp, 0x30
001DBFB4  mov      ebx, r9d
001DBFB7  mov      edi, r8d
001DBFBA  mov      esi, edx
001DBFBC  mov      ebp, ecx
001DBFBE  call     0x210b30  ; -> 00210B30 fn
001DBFC3  mov      rcx, rax
001DBFC6  mov      r9d, edi
001DBFC9  mov      eax, dword ptr [rsp + 0x60]
001DBFCD  mov      r8d, esi
001DBFD0  mov      dword ptr [rsp + 0x28], eax
001DBFD4  mov      edx, ebp
001DBFD6  mov      dword ptr [rsp + 0x20], ebx
001DBFDA  call     0x210e10  ; -> 00210E10 fn
001DBFDF  mov      rbx, qword ptr [rsp + 0x40]
001DBFE4  mov      rbp, qword ptr [rsp + 0x48]
001DBFE9  mov      rsi, qword ptr [rsp + 0x50]
001DBFEE  add      rsp, 0x30
001DBFF2  pop      rdi
001DBFF3  ret      
```

## 00204340 (87 B, extent 00204340-00204397)

Documented callee on this page: `002044C0`

```
00204340  mov      qword ptr [rsp + 8], rbx
00204345  push     rdi
00204346  sub      rsp, 0x20
0020434A  lea      rdi, [rcx + 0x80]
00204351  mov      rbx, rcx
00204354  mov      rdx, qword ptr [rdi]
00204357  test     rdx, rdx
0020435A  je       0x20437c  ; -> 0020437C
0020435C  mov      r8, qword ptr [rdi + 0x10]
00204360  mov      rcx, rdi
00204363  sub      r8, rdx
00204366  sar      r8, 4
0020436A  call     0x209b50  ; -> 00209B50 fn
0020436F  xor      eax, eax
00204371  mov      qword ptr [rdi], rax
00204374  mov      qword ptr [rdi + 8], rax
00204378  mov      qword ptr [rdi + 0x10], rax
0020437C  lea      rcx, [rbx + 0x40]
00204380  call     0x2044c0  ; -> 002044C0 fn
00204385  mov      rcx, rbx
00204388  mov      rbx, qword ptr [rsp + 0x30]
0020438D  add      rsp, 0x20
00204391  pop      rdi
00204392  jmp      0x2044c0  ; -> 002044C0 fn
```

## 002094D0 (81 B, extent 002094D0-00209521)

Documented callee on this page: `00209BC0`

```
002094D0  push     rbx
002094D2  sub      rsp, 0x20
002094D6  mov      rbx, rcx
002094D9  mov      rcx, qword ptr [rcx]
002094DC  test     rcx, rcx
002094DF  je       0x20951b  ; -> 0020951B
002094E1  mov      r8, qword ptr [rbx + 0x10]
002094E5  movabs   rax, 0x2aaaaaaaaaaaaaab
002094EF  sub      r8, rcx
002094F2  imul     r8
002094F5  sar      rdx, 2
002094F9  mov      r8, rdx
002094FC  shr      r8, 0x3f
00209500  add      r8, rdx
00209503  mov      rdx, rcx
00209506  mov      rcx, rbx
00209509  call     0x209bc0  ; -> 00209BC0 fn
0020950E  xor      eax, eax
00209510  mov      qword ptr [rbx], rax
00209513  mov      qword ptr [rbx + 8], rax
00209517  mov      qword ptr [rbx + 0x10], rax
0020951B  add      rsp, 0x20
0020951F  pop      rbx
00209520  ret      
```

## 00218CE0 (28 B, extent 00218CE0-00218CFC)

Documented callee on this page: `00221710`

```
00218CE0  push     rbx
00218CE2  sub      rsp, 0x20
00218CE6  mov      ebx, edx
00218CE8  call     0x221710  ; -> 00221710 fn
00218CED  mov      rcx, rax
00218CF0  mov      edx, ebx
00218CF2  add      rsp, 0x20
00218CF6  pop      rbx
00218CF7  jmp      0x221280  ; -> 00221280 fn
```

## 00219BC0 (122 B, extent 00219BC0-00219C3A)

Documented callee on this page: `00212950`

```
00219BC0  mov      qword ptr [rsp + 8], rbx
00219BC5  mov      qword ptr [rsp + 0x10], rbp
00219BCA  mov      qword ptr [rsp + 0x18], rsi
00219BCF  push     rdi
00219BD0  push     r14
00219BD2  push     r15
00219BD4  sub      rsp, 0x20
00219BD8  mov      rbx, qword ptr [rcx + 8]
00219BDC  lea      rsi, [rcx + 8]
00219BE0  xor      edi, edi
00219BE2  mov      r15, r8
00219BE5  mov      ebp, edx
00219BE7  cmp      rbx, rsi
00219BEA  je       0x219c01  ; -> 00219C01
00219BEC  nop      dword ptr [rax]
00219BF0  mov      rdi, qword ptr [rbx + 0x10]
00219BF4  cmp      dword ptr [rdi + 0x38], ebp
00219BF7  je       0x219c01  ; -> 00219C01
00219BF9  mov      rbx, qword ptr [rbx]
00219BFC  cmp      rbx, rsi
00219BFF  jne      0x219bf0  ; -> 00219BF0
00219C01  call     0x212950  ; -> 00212950 fn
00219C06  mov      r14d, eax
00219C09  cmp      rbx, rsi
00219C0C  je       0x219c21  ; -> 00219C21
00219C0E  mov      r9, r15
00219C11  mov      r8d, ebp
00219C14  mov      edx, eax
00219C16  mov      rcx, rdi
00219C19  call     0x223030  ; -> 00223030 fn
00219C1E  mov      eax, r14d
00219C21  mov      rbx, qword ptr [rsp + 0x40]
00219C26  mov      rbp, qword ptr [rsp + 0x48]
00219C2B  mov      rsi, qword ptr [rsp + 0x50]
00219C30  add      rsp, 0x20
00219C34  pop      r15
00219C36  pop      r14
00219C38  pop      rdi
00219C39  ret      
```

## 0021D640 (109 B, extent 0021D640-0021D6AD)

Documented callee on this page: `00225280`

```
0021D640  mov      qword ptr [rsp + 8], rbx
0021D645  mov      qword ptr [rsp + 0x10], rbp
0021D64A  mov      qword ptr [rsp + 0x18], rsi
0021D64F  mov      qword ptr [rsp + 0x20], rdi
0021D654  push     r14
0021D656  sub      rsp, 0x20
0021D65A  mov      rbx, qword ptr [rcx + 8]
0021D65E  lea      rsi, [rcx + 8]
0021D662  mov      ebp, r9d
0021D665  mov      r14d, r8d
0021D668  mov      edi, edx
0021D66A  cmp      rbx, rsi
0021D66D  je       0x21d692  ; -> 0021D692
0021D66F  nop      
0021D670  mov      rcx, qword ptr [rbx + 0x10]
0021D674  test     edi, edi
0021D676  js       0x21d67d  ; -> 0021D67D
0021D678  cmp      dword ptr [rcx + 0x38], edi
0021D67B  jne      0x21d68a  ; -> 0021D68A
0021D67D  mov      r9d, ebp
0021D680  mov      r8d, r14d
0021D683  mov      edx, edi
0021D685  call     0x225280  ; -> 00225280 fn
0021D68A  mov      rbx, qword ptr [rbx]
0021D68D  cmp      rbx, rsi
0021D690  jne      0x21d670  ; -> 0021D670
0021D692  mov      rbx, qword ptr [rsp + 0x30]
0021D697  mov      rbp, qword ptr [rsp + 0x38]
0021D69C  mov      rsi, qword ptr [rsp + 0x40]
0021D6A1  mov      rdi, qword ptr [rsp + 0x48]
0021D6A6  add      rsp, 0x20
0021D6AA  pop      r14
0021D6AC  ret      
```

## 00222490 (86 B, extent 00222490-002224E6)

Documented callee on this page: `002256F0`

```
00222490  mov      qword ptr [rsp + 8], rbx
00222495  mov      qword ptr [rsp + 0x10], rbp
0022249A  mov      qword ptr [rsp + 0x18], rsi
0022249F  push     rdi
002224A0  sub      rsp, 0x20
002224A4  mov      rbx, qword ptr [rcx + 8]
002224A8  lea      rdi, [rcx + 8]
002224AC  mov      esi, r8d
002224AF  mov      ebp, edx
002224B1  cmp      rbx, rdi
002224B4  je       0x2224d1  ; -> 002224D1
002224B6  mov      rcx, qword ptr [rbx + 0x10]
002224BA  test     rcx, rcx
002224BD  je       0x2224c9  ; -> 002224C9
002224BF  mov      r8d, esi
002224C2  mov      edx, ebp
002224C4  call     0x2256f0  ; -> 002256F0 fn
002224C9  mov      rbx, qword ptr [rbx]
002224CC  cmp      rbx, rdi
002224CF  jne      0x2224b6  ; -> 002224B6
002224D1  mov      rbx, qword ptr [rsp + 0x30]
002224D6  mov      rbp, qword ptr [rsp + 0x38]
002224DB  mov      rsi, qword ptr [rsp + 0x40]
002224E0  add      rsp, 0x20
002224E4  pop      rdi
002224E5  ret      
```

## 00222AD0 (65 B, extent 00222AD0-00222B11)

Documented callee on this page: `007A7010`

```
00222AD0  mov      qword ptr [rsp + 8], rbx
00222AD5  push     rdi
00222AD6  sub      rsp, 0x20
00222ADA  lea      rbx, [rcx + 0x38]
00222ADE  mov      edi, edx
00222AE0  mov      rcx, rbx
00222AE3  call     0x7a9250  ; -> 007A9250 fn
00222AE8  mov      rcx, rbx
00222AEB  call     0x7a7010  ; -> 007A7010 fn
00222AF0  test     eax, eax
00222AF2  je       0x222b06  ; -> 00222B06
00222AF4  movss    xmm2, dword ptr [rip + 0x1ac9174]  ; -> 01CEBC70 [f32 4]
00222AFC  mov      edx, edi
00222AFE  mov      rcx, rbx
00222B01  call     0x7a9650  ; -> 007A9650 fn
00222B06  mov      rbx, qword ptr [rsp + 0x30]
00222B0B  add      rsp, 0x20
00222B0F  pop      rdi
00222B10  ret      
```

## 00223060 (110 B, extent 00223060-002230CE)

Documented callee on this page: `002256F0`

```
00223060  mov      qword ptr [rsp + 8], rbx
00223065  push     rdi
00223066  sub      rsp, 0x20
0022306A  mov      edi, r9d
0022306D  test     edx, edx
0022306F  je       0x2230a4  ; -> 002230A4
00223071  call     0x221ed0  ; -> 00221ED0 fn
00223076  mov      rbx, rax
00223079  test     rax, rax
0022307C  je       0x2230c1  ; -> 002230C1
0022307E  mov      rcx, rax
00223081  call     0x225680  ; -> 00225680 fn
00223086  test     eax, eax
00223088  je       0x2230c1  ; -> 002230C1
0022308A  xor      r8d, r8d
0022308D  mov      edx, edi
0022308F  mov      rcx, rbx
00223092  call     0x2256f0  ; -> 002256F0 fn
00223097  mov      al, 1
00223099  mov      rbx, qword ptr [rsp + 0x30]
0022309E  add      rsp, 0x20
002230A2  pop      rdi
002230A3  ret      
002230A4  cmp      dword ptr [rcx + 0x38], r8d
002230A8  jne      0x2230c1  ; -> 002230C1
002230AA  xor      r8d, r8d
002230AD  mov      edx, edi
002230AF  call     0x222490  ; -> 00222490 fn
002230B4  mov      al, 1
002230B6  mov      rbx, qword ptr [rsp + 0x30]
002230BB  add      rsp, 0x20
002230BF  pop      rdi
002230C0  ret      
002230C1  xor      al, al
002230C3  mov      rbx, qword ptr [rsp + 0x30]
002230C8  add      rsp, 0x20
002230CC  pop      rdi
002230CD  ret      
```

## 00223EE0 (91 B, extent 00223EE0-00223F3B)

Documented callee on this page: `002256F0`

```
00223EE0  mov      qword ptr [rsp + 8], rbx
00223EE5  push     rdi
00223EE6  sub      rsp, 0x20
00223EEA  mov      edi, r9d
00223EED  test     edx, edx
00223EEF  je       0x223ef8  ; -> 00223EF8
00223EF1  call     0x221ed0  ; -> 00221ED0 fn
00223EF6  jmp      0x223f00  ; -> 00223F00
00223EF8  mov      edx, r8d
00223EFB  call     0x221e60  ; -> 00221E60 fn
00223F00  mov      rbx, rax
00223F03  test     rax, rax
00223F06  je       0x223f2e  ; -> 00223F2E
00223F08  mov      rcx, rax
00223F0B  call     0x225680  ; -> 00225680 fn
00223F10  test     eax, eax
00223F12  je       0x223f2e  ; -> 00223F2E
00223F14  xor      r8d, r8d
00223F17  mov      edx, edi
00223F19  mov      rcx, rbx
00223F1C  call     0x2256f0  ; -> 002256F0 fn
00223F21  mov      al, 1
00223F23  mov      rbx, qword ptr [rsp + 0x30]
00223F28  add      rsp, 0x20
00223F2C  pop      rdi
00223F2D  ret      
00223F2E  xor      al, al
00223F30  mov      rbx, qword ptr [rsp + 0x30]
00223F35  add      rsp, 0x20
00223F39  pop      rdi
00223F3A  ret      
```

## 002254F0 (125 B, extent 002254F0-0022556D)

Documented callee on this page: `00221710`

```
002254F0  mov      qword ptr [rsp + 8], rbx
002254F5  push     rdi
002254F6  sub      rsp, 0x20
002254FA  mov      rbx, rcx
002254FD  add      rcx, 8
00225501  call     0x7a8ca0  ; -> 007A8CA0 fn
00225506  test     al, al
00225508  je       0x225524  ; -> 00225524
0022550A  nop      word ptr [rax + rax]
00225510  xor      ecx, ecx
00225512  call     0x5ccb80  ; -> 005CCB80 fn
00225517  lea      rcx, [rbx + 8]
0022551B  call     0x7a8ca0  ; -> 007A8CA0 fn
00225520  test     al, al
00225522  jne      0x225510  ; -> 00225510
00225524  mov      rcx, qword ptr [rbx + 0x20]
00225528  mov      rdi, qword ptr [rbx + 0x28]
0022552C  test     rcx, rcx
0022552F  je       0x22553e  ; -> 0022553E
00225531  call     0x809950  ; -> 00809950 fn
00225536  mov      qword ptr [rbx + 0x20], 0
0022553E  test     rdi, rdi
00225541  je       0x225553  ; -> 00225553
00225543  mov      rcx, rdi
00225546  call     0x809950  ; -> 00809950 fn
0022554B  mov      qword ptr [rbx + 0x28], 0
00225553  call     0x221710  ; -> 00221710 fn
00225558  mov      rcx, rax
0022555B  mov      rdx, rbx
0022555E  mov      rbx, qword ptr [rsp + 0x30]
00225563  add      rsp, 0x20
00225567  pop      rdi
00225568  jmp      0x2211b0  ; -> 002211B0 fn
```

## 002BC2C0 (65 B, extent 002BC2C0-002BC301)

Documented callee on this page: `002814E0`

```
002BC2C0  sub      rsp, 0x28
002BC2C4  cmp      qword ptr [rip + 0x1de2324], 0  ; -> 0209E5F0
002BC2CC  jne      0x2bc2fc  ; -> 002BC2FC
002BC2CE  cmp      qword ptr [rip + 0x1de2322], 0  ; -> 0209E5F8
002BC2D6  jne      0x2bc2fc  ; -> 002BC2FC
002BC2D8  call     0x402220  ; -> 00402220 fn
002BC2DD  test     rax, rax
002BC2E0  jne      0x2bc2fc  ; -> 002BC2FC
002BC2E2  lea      rcx, [rip + 0x1de231f]  ; -> 0209E608
002BC2E9  call     0x285f00  ; -> 00285F00 fn
002BC2EE  mov      ecx, 0x417
002BC2F3  add      rsp, 0x28
002BC2F7  jmp      0x2814e0  ; -> 002814E0 fn
002BC2FC  add      rsp, 0x28
002BC300  ret      
```

## 00341710 (75 B, extent 00341710-0034175B)

Documented callee on this page: `00360C20`

```
00341710  mov      qword ptr [rsp + 8], rbx
00341715  push     rdi
00341716  sub      rsp, 0x20
0034171A  mov      rcx, r9
0034171D  mov      rbx, rdx
00341720  call     0x267e10  ; -> 00267E10 fn
00341725  movzx    ecx, byte ptr [rbx + 0x15]
00341729  mov      edi, eax
0034172B  call     0x267310  ; -> 00267310 fn
00341730  test     eax, eax
00341732  jne      0x341750  ; -> 00341750
00341734  mov      ecx, edi
00341736  call     0x360c20  ; -> 00360C20 fn
0034173B  test     eax, eax
0034173D  jns      0x341749  ; -> 00341749
0034173F  mov      ecx, 1
00341744  call     0x314d40  ; -> 00314D40 fn
00341749  mov      ecx, edi
0034174B  call     0x361630  ; -> 00361630 fn
00341750  mov      rbx, qword ptr [rsp + 0x30]
00341755  add      rsp, 0x20
00341759  pop      rdi
0034175A  ret      
```

## 00360EE0 (303 B, extent 00360EE0-0036100F)

Documented callee on this page: `002DEC30`

```
00360EE0  mov      qword ptr [rsp + 0x10], rbp
00360EE5  mov      qword ptr [rsp + 0x18], rsi
00360EEA  mov      qword ptr [rsp + 0x20], rdi
00360EEF  push     r12
00360EF1  push     r14
00360EF3  push     r15
00360EF5  sub      rsp, 0x20
00360EF9  mov      r15d, dword ptr [rcx + 0x28]
00360EFD  mov      rdi, rcx
00360F00  mov      edx, dword ptr [rcx]
00360F02  mov      eax, r15d
00360F05  mov      r14d, dword ptr [rcx + 0x30]
00360F09  mov      ebp, dword ptr [rcx + 0x38]
00360F0C  sar      eax, 0x10
00360F0F  movzx    esi, r15w
00360F13  movzx    r12d, al
00360F17  test     edx, edx
00360F19  je       0x360f34  ; -> 00360F34
00360F1B  sub      edx, 1
00360F1E  je       0x360f3a  ; -> 00360F3A
00360F20  sub      edx, 1
00360F23  je       0x360f47  ; -> 00360F47
00360F25  sub      edx, 1
00360F28  je       0x360f98  ; -> 00360F98
00360F2A  cmp      edx, 1
00360F2D  je       0x360f9e  ; -> 00360F9E
00360F2F  jmp      0x360ff5  ; -> 00360FF5
00360F34  mov      dword ptr [rcx], 1
00360F3A  mov      ecx, esi
00360F3C  call     0x361630  ; -> 00361630 fn
00360F41  mov      dword ptr [rdi], 2
00360F47  xor      ecx, ecx
00360F49  lea      r9, [rip + 0x1f6aaa0]  ; -> 022CB9F0
00360F50  mov      rdx, r9
00360F53  lea      r8d, [rcx - 5]
00360F57  cmp      byte ptr [rdx], 0
00360F5A  je       0x360f66  ; -> 00360F66
00360F5C  movzx    eax, byte ptr [rdx + 1]
00360F60  cmp      eax, esi
00360F62  je       0x360f80  ; -> 00360F80
00360F64  jmp      0x360f72  ; -> 00360F72
00360F66  cmp      r8d, -5
00360F6A  jne      0x360f72  ; -> 00360F72
00360F6C  mov      r8d, ecx
00360F6F  not      r8d
00360F72  inc      ecx
00360F74  add      rdx, 0x18
00360F78  cmp      ecx, 4
00360F7B  jl       0x360f57  ; -> 00360F57
00360F7D  mov      ecx, r8d
00360F80  test     ecx, ecx
00360F82  js       0x360ff5  ; -> 00360FF5
00360F84  movsxd   rax, ecx
00360F87  lea      rcx, [rax + rax*2]
00360F8B  cmp      byte ptr [r9 + rcx*8], 5
00360F90  jne      0x360ff5  ; -> 00360FF5
00360F92  mov      dword ptr [rdi], 3
00360F98  mov      dword ptr [rdi], 4
00360F9E  mov      qword ptr [rsp + 0x40], rbx
00360FA3  call     0x2dec00  ; -> 002DEC00 fn
00360FA8  mov      ebx, eax
00360FAA  mov      ecx, esi
00360FAC  test     eax, eax
00360FAE  js       0x360fba  ; -> 00360FBA
00360FB0  mov      edx, r14d
00360FB3  call     0x2dec30  ; -> 002DEC30 fn
00360FB8  jmp      0x360fd9  ; -> 00360FD9
00360FBA  mov      edx, r12d
00360FBD  call     0x2dee30  ; -> 002DEE30 fn
00360FC2  mov      ecx, esi
00360FC4  test     r15d, 0xff000000
00360FCB  je       0x360fd4  ; -> 00360FD4
00360FCD  call     0x2dedb0  ; -> 002DEDB0 fn
00360FD2  jmp      0x360fd9  ; -> 00360FD9
00360FD4  call     0x2ded30  ; -> 002DED30 fn
00360FD9  test     ebp, ebp
00360FDB  je       0x360fea  ; -> 00360FEA
00360FDD  mov      r8d, ebp
00360FE0  mov      edx, r14d
00360FE3  mov      ecx, ebx
00360FE5  call     0x361170  ; -> 00361170 fn
00360FEA  mov      rbx, qword ptr [rsp + 0x40]
00360FEF  mov      dword ptr [rdi], 5
00360FF5  mov      rbp, qword ptr [rsp + 0x48]
00360FFA  mov      rsi, qword ptr [rsp + 0x50]
00360FFF  mov      rdi, qword ptr [rsp + 0x58]
00361004  add      rsp, 0x20
00361008  pop      r15
0036100A  pop      r14
0036100C  pop      r12
0036100E  ret      
```

## 00363A20 (88 B, extent 00363A20-00363A78)

Documented callee on this page: `002DEF40`

```
00363A20  sub      rsp, 0x28
00363A24  dec      ecx
00363A26  cmp      ecx, 2
00363A29  ja       0x363a73  ; -> 00363A73
00363A2B  movsxd   rax, ecx
00363A2E  lea      rcx, [rip + 0x1f68123]  ; -> 022CBB58
00363A35  mov      qword ptr [rsp + 0x20], rbx
00363A3A  mov      ebx, dword ptr [rcx + rax*4]
00363A3D  test     ebx, ebx
00363A3F  js       0x363a6e  ; -> 00363A6E
00363A41  movzx    r8d, byte ptr [rip + 0x1f68049]  ; -> 022CBA92
00363A49  mov      edx, 0x40
00363A4E  mov      ecx, ebx
00363A50  call     0x2def40  ; -> 002DEF40 fn
00363A55  mov      dword ptr [rip + 0x1f68015], eax  ; -> 022CBA70
00363A5B  movzx    eax, byte ptr [rip + 0x1f68030]  ; -> 022CBA92
00363A62  mov      byte ptr [rip + 0x1f6802b], al  ; -> 022CBA93
00363A68  mov      dword ptr [rip + 0x1f6800e], ebx  ; -> 022CBA7C
00363A6E  mov      rbx, qword ptr [rsp + 0x20]
00363A73  add      rsp, 0x28
00363A77  ret      
```

## 003DF130 (197 B, extent 003DF130-003DF1F5)

Documented callee on this page: `002DEF40`

```
003DF130  sub      rsp, 0x28
003DF134  lea      r11, [rip + 0x277a225]  ; -> 02B59360
003DF13B  cmp      edx, 7
003DF13E  ja       0x3df153  ; -> 003DF153
003DF140  movsxd   rax, edx
003DF143  movsxd   r10, ecx
003DF146  lea      r10, [rax + r10*8]
003DF14A  imul     rax, r10, 0x38
003DF14E  add      rax, r11
003DF151  jmp      0x3df155  ; -> 003DF155
003DF153  xor      eax, eax
003DF155  movzx    eax, byte ptr [rax + 0x10]
003DF159  dec      al
003DF15B  test     al, 0xfb
003DF15D  jne      0x3df1ee  ; -> 003DF1EE
003DF163  mov      qword ptr [rsp + 0x30], rbx
003DF168  cmp      edx, 7
003DF16B  ja       0x3df180  ; -> 003DF180
003DF16D  movsxd   rcx, ecx
003DF170  movsxd   rax, edx
003DF173  lea      rcx, [rax + rcx*8]
003DF177  imul     rbx, rcx, 0x38
003DF17B  add      rbx, r11
003DF17E  jmp      0x3df182  ; -> 003DF182
003DF180  xor      ebx, ebx
003DF182  mov      rbx, qword ptr [rbx + 8]
003DF186  cmp      r8d, dword ptr [rbx + 4]
003DF18A  jge      0x3df1e2  ; -> 003DF1E2
003DF18C  mov      qword ptr [rsp + 0x38], rsi
003DF191  mov      edx, r9d
003DF194  mov      qword ptr [rsp + 0x20], rdi
003DF199  movsxd   rdi, r8d
003DF19C  mov      r8d, dword ptr [rsp + 0x50]
003DF1A1  mov      ecx, dword ptr [rbx + rdi*4 + 0x20]
003DF1A5  call     0x2def40  ; -> 002DEF40 fn
003DF1AA  mov      esi, eax
003DF1AC  or       ecx, 0xffffffff
003DF1AF  movzx    eax, word ptr [rbx + 0x18]
003DF1B3  test     ax, ax
003DF1B6  je       0x3df1c2  ; -> 003DF1C2
003DF1B8  movzx    ecx, ax
003DF1BB  add      rcx, rbx
003DF1BE  movsx    ecx, word ptr [rcx + rdi*2]
003DF1C2  call     0x314d50  ; -> 00314D50 fn
003DF1C7  call     0x314000  ; -> 00314000 fn
003DF1CC  mov      rdi, qword ptr [rsp + 0x20]
003DF1D1  mov      eax, esi
003DF1D3  mov      rsi, qword ptr [rsp + 0x38]
003DF1D8  mov      rbx, qword ptr [rsp + 0x30]
003DF1DD  add      rsp, 0x28
003DF1E1  ret      
003DF1E2  xor      eax, eax
003DF1E4  mov      rbx, qword ptr [rsp + 0x30]
003DF1E9  add      rsp, 0x28
003DF1ED  ret      
003DF1EE  xor      eax, eax
003DF1F0  add      rsp, 0x28
003DF1F4  ret      
```

## 003DF200 (189 B, extent 003DF200-003DF2BD)

Documented callee on this page: `002DF010`

```
003DF200  sub      rsp, 0x28
003DF204  lea      r10, [rip + 0x277a155]  ; -> 02B59360
003DF20B  cmp      edx, 7
003DF20E  ja       0x3df223  ; -> 003DF223
003DF210  movsxd   rax, edx
003DF213  movsxd   r9, ecx
003DF216  lea      r9, [rax + r9*8]
003DF21A  imul     rax, r9, 0x38
003DF21E  add      rax, r10
003DF221  jmp      0x3df225  ; -> 003DF225
003DF223  xor      eax, eax
003DF225  movzx    eax, byte ptr [rax + 0x10]
003DF229  dec      al
003DF22B  test     al, 0xfb
003DF22D  jne      0x3df2b6  ; -> 003DF2B6
003DF233  mov      qword ptr [rsp + 0x30], rbx
003DF238  cmp      edx, 7
003DF23B  ja       0x3df250  ; -> 003DF250
003DF23D  movsxd   rcx, ecx
003DF240  movsxd   rax, edx
003DF243  lea      rcx, [rax + rcx*8]
003DF247  imul     rbx, rcx, 0x38
003DF24B  add      rbx, r10
003DF24E  jmp      0x3df252  ; -> 003DF252
003DF250  xor      ebx, ebx
003DF252  mov      rbx, qword ptr [rbx + 8]
003DF256  cmp      r8d, dword ptr [rbx + 4]
003DF25A  jge      0x3df2aa  ; -> 003DF2AA
003DF25C  mov      qword ptr [rsp + 0x38], rsi
003DF261  mov      qword ptr [rsp + 0x20], rdi
003DF266  movsxd   rdi, r8d
003DF269  mov      ecx, dword ptr [rbx + rdi*4 + 0x20]
003DF26D  call     0x2df010  ; -> 002DF010 fn
003DF272  mov      esi, eax
003DF274  or       ecx, 0xffffffff
003DF277  movzx    eax, word ptr [rbx + 0x18]
003DF27B  test     ax, ax
003DF27E  je       0x3df28a  ; -> 003DF28A
003DF280  movzx    ecx, ax
003DF283  add      rcx, rbx
003DF286  movsx    ecx, word ptr [rcx + rdi*2]
003DF28A  call     0x314d50  ; -> 00314D50 fn
003DF28F  call     0x314000  ; -> 00314000 fn
003DF294  mov      rdi, qword ptr [rsp + 0x20]
003DF299  mov      eax, esi
003DF29B  mov      rsi, qword ptr [rsp + 0x38]
003DF2A0  mov      rbx, qword ptr [rsp + 0x30]
003DF2A5  add      rsp, 0x28
003DF2A9  ret      
003DF2AA  xor      eax, eax
003DF2AC  mov      rbx, qword ptr [rsp + 0x30]
003DF2B1  add      rsp, 0x28
003DF2B5  ret      
003DF2B6  xor      eax, eax
003DF2B8  add      rsp, 0x28
003DF2BC  ret      
```

## 00408360 (75 B, extent 00408360-004083AB)

Documented callee on this page: `00246AD0`

```
00408360  push     rbx
00408362  sub      rsp, 0x20
00408366  mov      rcx, qword ptr [rip + 0x275aa13]  ; -> 02B62D80
0040836D  test     rcx, rcx
00408370  je       0x408384  ; -> 00408384
00408372  test     byte ptr [rcx + 0xc8], 2
00408379  mov      rbx, qword ptr [rcx + 0xc0]
00408380  jne      0x4083a5  ; -> 004083A5
00408382  jmp      0x408386  ; -> 00408386
00408384  xor      ebx, ebx
00408386  test     rbx, rbx
00408389  je       0x4083a5  ; -> 004083A5
0040838B  mov      rdx, rbx
0040838E  call     0x246ad0  ; -> 00246AD0 fn
00408393  mov      eax, dword ptr [rbx + 0xd8]
00408399  and      eax, 0xfffffff7
0040839C  or       eax, 4
0040839F  mov      dword ptr [rbx + 0xd8], eax
004083A5  add      rsp, 0x20
004083A9  pop      rbx
004083AA  ret      
```

## 00675440 (31 B, extent 00675440-0067545F)

Documented callee on this page: `00195200`

```
00675440  push     rbx
00675442  sub      rsp, 0x20
00675446  mov      rbx, rcx
00675449  add      rcx, 0x20
0067544D  call     0x195200  ; -> 00195200 fn
00675452  mov      rcx, rbx
00675455  add      rsp, 0x20
00675459  pop      rbx
0067545A  jmp      0x195200  ; -> 00195200 fn
```
