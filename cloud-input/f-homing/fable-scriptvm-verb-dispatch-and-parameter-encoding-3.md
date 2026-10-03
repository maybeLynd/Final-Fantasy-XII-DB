# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 00352040 (57 B, extent 00352040-00352079)

Documented callee on this page: `00267DB0`

```
00352040  push     rbx
00352042  sub      rsp, 0x30
00352046  mov      rcx, r9
00352049  movaps   xmmword ptr [rsp + 0x20], xmm6
0035204E  mov      rbx, rdx
00352051  call     0x267db0  ; -> 00267DB0 fn
00352056  movaps   xmm1, xmm0
00352059  mov      rcx, rbx
0035205C  movaps   xmm6, xmm0
0035205F  call     0x26d6a0  ; -> 0026D6A0 fn
00352064  movaps   xmm1, xmm6
00352067  mov      rcx, rbx
0035206A  movaps   xmm6, xmmword ptr [rsp + 0x20]
0035206F  add      rsp, 0x30
00352073  pop      rbx
00352074  jmp      0x26a640  ; -> 0026A640 fn
```

## 00352130 (61 B, extent 00352130-0035216D)

Documented callee on this page: `002640C0`

```
00352130  mov      qword ptr [rsp + 8], rbx
00352135  push     rdi
00352136  sub      rsp, 0x20
0035213A  mov      rcx, r9
0035213D  mov      rbx, r9
00352140  call     0x267e10  ; -> 00267E10 fn
00352145  mov      rcx, rbx
00352148  mov      edi, eax
0035214A  call     0x267e10  ; -> 00267E10 fn
0035214F  mov      ebx, eax
00352151  call     0x2640c0  ; -> 002640C0 fn
00352156  mov      r8d, edi
00352159  mov      edx, ebx
0035215B  mov      ecx, dword ptr [rax + 0x28]
0035215E  mov      rbx, qword ptr [rsp + 0x30]
00352163  add      rsp, 0x20
00352167  pop      rdi
00352168  jmp      0x3de9a0  ; -> 003DE9A0 fn
```

## 00352810 (129 B, extent 00352810-00352891)

Documented callee on this page: `00267DB0`

```
00352810  mov      qword ptr [rsp + 8], rbx
00352815  push     rdi
00352816  sub      rsp, 0x50
0035281A  movaps   xmmword ptr [rsp + 0x40], xmm6
0035281F  mov      rcx, r9
00352822  movaps   xmmword ptr [rsp + 0x30], xmm7
00352827  mov      rbx, r9
0035282A  movaps   xmmword ptr [rsp + 0x20], xmm8
00352830  mov      rdi, rdx
00352833  call     0x267db0  ; -> 00267DB0 fn
00352838  mov      rcx, rbx
0035283B  movaps   xmm8, xmm0
0035283F  call     0x267db0  ; -> 00267DB0 fn
00352844  mov      rcx, rbx
00352847  movaps   xmm7, xmm0
0035284A  call     0x267db0  ; -> 00267DB0 fn
0035284F  mov      rcx, rbx
00352852  movaps   xmm6, xmm0
00352855  call     0x267db0  ; -> 00267DB0 fn
0035285A  movaps   xmm2, xmm6
0035285D  movaps   xmm1, xmm0
00352860  mov      rcx, rdi
00352863  call     0x26bff0  ; -> 0026BFF0 fn
00352868  movaps   xmm2, xmm8
0035286C  movaps   xmm1, xmm7
0035286F  mov      rcx, rdi
00352872  mov      rbx, qword ptr [rsp + 0x60]
00352877  movaps   xmm6, xmmword ptr [rsp + 0x40]
0035287C  movaps   xmm7, xmmword ptr [rsp + 0x30]
00352881  movaps   xmm8, xmmword ptr [rsp + 0x20]
00352887  add      rsp, 0x50
0035288B  pop      rdi
0035288C  jmp      0x26bd50  ; -> 0026BD50 fn
```

## 00352980 (46 B, extent 00352980-003529AE)

Documented callee on this page: `003DB420`

```
00352980  push     rbx
00352982  sub      rsp, 0x20
00352986  mov      rcx, r9
00352989  mov      rbx, rdx
0035298C  call     0x267e10  ; -> 00267E10 fn
00352991  mov      r8d, 4
00352997  mov      edx, eax
00352999  mov      rcx, rbx
0035299C  call     0x3db420  ; -> 003DB420 fn
003529A1  mov      rcx, rbx
003529A4  add      rsp, 0x20
003529A8  pop      rbx
003529A9  jmp      0x3db6e0  ; -> 003DB6E0 fn
```

## 00352C00 (126 B, extent 00352C00-00352C7E)

Documented callee on this page: `0026B0C0`

```
00352C00  mov      qword ptr [rsp + 8], rbx
00352C05  push     rdi
00352C06  sub      rsp, 0x40
00352C0A  movaps   xmmword ptr [rsp + 0x30], xmm6
00352C0F  mov      rcx, r9
00352C12  movaps   xmmword ptr [rsp + 0x20], xmm7
00352C17  mov      rbx, r9
00352C1A  mov      rdi, rdx
00352C1D  call     0x267db0  ; -> 00267DB0 fn
00352C22  mov      rcx, rbx
00352C25  movaps   xmm6, xmm0
00352C28  call     0x267db0  ; -> 00267DB0 fn
00352C2D  movaps   xmm2, xmm6
00352C30  movaps   xmm1, xmm0
00352C33  mov      rcx, rdi
00352C36  call     0x26bff0  ; -> 0026BFF0 fn
00352C3B  mov      rcx, rbx
00352C3E  call     0x267db0  ; -> 00267DB0 fn
00352C43  mov      rcx, rbx
00352C46  movaps   xmm7, xmm0
00352C49  call     0x267db0  ; -> 00267DB0 fn
00352C4E  mov      rcx, rbx
00352C51  movaps   xmm6, xmm0
00352C54  call     0x267db0  ; -> 00267DB0 fn
00352C59  movaps   xmm3, xmm7
00352C5C  movaps   xmm2, xmm6
00352C5F  movaps   xmm1, xmm0
00352C62  mov      rcx, rdi
00352C65  mov      rbx, qword ptr [rsp + 0x50]
00352C6A  movaps   xmm6, xmmword ptr [rsp + 0x30]
00352C6F  movaps   xmm7, xmmword ptr [rsp + 0x20]
00352C74  add      rsp, 0x40
00352C78  pop      rdi
00352C79  jmp      0x26b0c0  ; -> 0026B0C0 fn
```

## 003531E0 (88 B, extent 003531E0-00353238)

Documented callee on this page: `0026B620`

```
003531E0  mov      qword ptr [rsp + 8], rbx
003531E5  mov      qword ptr [rsp + 0x10], rbp
003531EA  mov      qword ptr [rsp + 0x18], rsi
003531EF  push     rdi
003531F0  sub      rsp, 0x20
003531F4  mov      rbp, rcx
003531F7  mov      rbx, r9
003531FA  mov      rcx, r9
003531FD  mov      rdi, r8
00353200  mov      rsi, rdx
00353203  call     0x267db0  ; -> 00267DB0 fn
00353208  movaps   xmm1, xmm0
0035320B  mov      rcx, rsi
0035320E  call     0x26b620  ; -> 0026B620 fn
00353213  mov      r9, rbx
00353216  mov      r8, rdi
00353219  mov      rdx, rsi
0035321C  mov      rcx, rbp
0035321F  mov      rbx, qword ptr [rsp + 0x30]
00353224  mov      rbp, qword ptr [rsp + 0x38]
00353229  mov      rsi, qword ptr [rsp + 0x40]
0035322E  add      rsp, 0x20
00353232  pop      rdi
00353233  jmp      0x352c00  ; -> 00352C00 fn
```

## 00353490 (94 B, extent 00353490-003534EE)

Documented callee on this page: `00377AB0`

```
00353490  mov      qword ptr [rsp + 0x10], rbx
00353495  push     rdi
00353496  sub      rsp, 0x40
0035349A  mov      rax, qword ptr [rip + 0x1bf138f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003534A1  xor      rax, rsp
003534A4  mov      qword ptr [rsp + 0x30], rax
003534A9  mov      rbx, r9
003534AC  mov      rdi, rcx
003534AF  call     0x2640c0  ; -> 002640C0 fn
003534B4  mov      rcx, rbx
003534B7  call     0x267e10  ; -> 00267E10 fn
003534BC  lea      rdx, [rsp + 0x20]
003534C1  mov      ecx, eax
003534C3  call     0x377ab0  ; -> 00377AB0 fn
003534C8  movss    xmm1, dword ptr [rsp + 0x2c]
003534CE  mov      rcx, rdi
003534D1  call     0x26b4c0  ; -> 0026B4C0 fn
003534D6  mov      rcx, qword ptr [rsp + 0x30]
003534DB  xor      rcx, rsp
003534DE  call     0x808c40  ; -> 00808C40 fn
003534E3  mov      rbx, qword ptr [rsp + 0x58]
003534E8  add      rsp, 0x40
003534EC  pop      rdi
003534ED  ret      
```

## 00353660 (76 B, extent 00353660-003536AC)

Documented callee on this page: `003DB420`

```
00353660  mov      qword ptr [rsp + 8], rbx
00353665  push     rdi
00353666  sub      rsp, 0x20
0035366A  mov      rcx, r9
0035366D  mov      rbx, r9
00353670  call     0x267e10  ; -> 00267E10 fn
00353675  mov      rcx, rbx
00353678  mov      edi, eax
0035367A  call     0x267e10  ; -> 00267E10 fn
0035367F  mov      ecx, eax
00353681  call     0x264010  ; -> 00264010 fn
00353686  mov      r8d, 4
0035368C  lea      edx, [rdi + 1]
0035368F  mov      rcx, rax
00353692  mov      rbx, rax
00353695  call     0x3db420  ; -> 003DB420 fn
0035369A  mov      rcx, rbx
0035369D  mov      rbx, qword ptr [rsp + 0x30]
003536A2  add      rsp, 0x20
003536A6  pop      rdi
003536A7  jmp      0x3db6e0  ; -> 003DB6E0 fn
```

## 00353BF0 (35 B, extent 00353BF0-00353C13)

Documented callee on this page: `002640C0`

```
00353BF0  push     rbx
00353BF2  sub      rsp, 0x20
00353BF6  mov      rbx, rdx
00353BF9  call     0x2640c0  ; -> 002640C0 fn
00353BFE  movzx    edx, word ptr [rbx]
00353C01  mov      ecx, dword ptr [rax + 0x28]
00353C04  call     0x263a30  ; -> 00263A30 fn
00353C09  add      rsp, 0x20
00353C0D  pop      rbx
00353C0E  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 00353ED0 (236 B, extent 00353ED0-00353FBC)

Documented callee on this page: `00377900`

```
00353ED0  mov      qword ptr [rsp + 0x10], rbx
00353ED5  push     rbp
00353ED6  push     rsi
00353ED7  push     rdi
00353ED8  push     r14
00353EDA  push     r15
00353EDC  sub      rsp, 0x40
00353EE0  mov      rax, qword ptr [rip + 0x1bf0949]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00353EE7  xor      rax, rsp
00353EEA  mov      qword ptr [rsp + 0x30], rax
00353EEF  mov      r15, r9
00353EF2  mov      rbp, rcx
00353EF5  call     0x2640c0  ; -> 002640C0 fn
00353EFA  mov      rcx, r15
00353EFD  mov      rbx, rax
00353F00  call     0x267e10  ; -> 00267E10 fn
00353F05  mov      r8d, eax
00353F08  mov      rdx, rbp
00353F0B  mov      rcx, rbx
00353F0E  call     0x2650b0  ; -> 002650B0 fn
00353F13  mov      rcx, r15
00353F16  mov      r14, rax
00353F19  call     0x267e10  ; -> 00267E10 fn
00353F1E  mov      r8d, eax
00353F21  mov      rdx, rbp
00353F24  mov      rcx, rbx
00353F27  call     0x2650b0  ; -> 002650B0 fn
00353F2C  mov      rcx, r15
00353F2F  mov      rsi, rax
00353F32  call     0x267e10  ; -> 00267E10 fn
00353F37  mov      r8d, eax
00353F3A  mov      rdx, rbp
00353F3D  mov      rcx, rbx
00353F40  call     0x2650b0  ; -> 002650B0 fn
00353F45  mov      rcx, r15
00353F48  mov      rdi, rax
00353F4B  call     0x267e10  ; -> 00267E10 fn
00353F50  mov      r8d, eax
00353F53  mov      rdx, rbp
00353F56  mov      rcx, rbx
00353F59  call     0x2650b0  ; -> 002650B0 fn
00353F5E  mov      rcx, r15
00353F61  mov      rbx, rax
00353F64  call     0x267e10  ; -> 00267E10 fn
00353F69  lea      rdx, [rsp + 0x20]
00353F6E  mov      ecx, eax
00353F70  call     0x377900  ; -> 00377900 fn
00353F75  movss    xmm0, dword ptr [rsp + 0x20]
00353F7B  movss    dword ptr [rbx], xmm0
00353F7F  movss    xmm1, dword ptr [rsp + 0x24]
00353F85  movss    dword ptr [rdi], xmm1
00353F89  movss    xmm0, dword ptr [rsp + 0x28]
00353F8F  movss    dword ptr [rsi], xmm0
00353F93  movss    xmm1, dword ptr [rsp + 0x2c]
00353F99  movss    dword ptr [r14], xmm1
00353F9E  mov      rcx, qword ptr [rsp + 0x30]
00353FA3  xor      rcx, rsp
00353FA6  call     0x808c40  ; -> 00808C40 fn
00353FAB  mov      rbx, qword ptr [rsp + 0x78]
00353FB0  add      rsp, 0x40
00353FB4  pop      r15
00353FB6  pop      r14
00353FB8  pop      rdi
00353FB9  pop      rsi
00353FBA  pop      rbp
00353FBB  ret      
```

## 003540B0 (87 B, extent 003540B0-00354107)

Documented callee on this page: `002650B0`

```
003540B0  mov      qword ptr [rsp + 8], rbx
003540B5  mov      qword ptr [rsp + 0x10], rsi
003540BA  push     rdi
003540BB  sub      rsp, 0x20
003540BF  mov      rdi, r9
003540C2  mov      rsi, rdx
003540C5  call     0x2640c0  ; -> 002640C0 fn
003540CA  mov      rcx, rdi
003540CD  mov      rbx, rax
003540D0  call     0x267e10  ; -> 00267E10 fn
003540D5  mov      r8d, eax
003540D8  mov      rdx, rsi
003540DB  mov      rcx, rbx
003540DE  call     0x2650b0  ; -> 002650B0 fn
003540E3  call     0x2640c0  ; -> 002640C0 fn
003540E8  movzx    edx, word ptr [rsi]
003540EB  mov      ecx, dword ptr [rax + 0x28]
003540EE  call     0x263a30  ; -> 00263A30 fn
003540F3  mov      rbx, qword ptr [rsp + 0x30]
003540F8  mov      rsi, qword ptr [rsp + 0x38]
003540FD  add      rsp, 0x20
00354101  pop      rdi
00354102  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 003546C0 (34 B, extent 003546C0-003546E2)

Documented callee on this page: `002640C0`

```
003546C0  sub      rsp, 0x28
003546C4  call     0x2640c0  ; -> 002640C0 fn
003546C9  xor      ecx, ecx
003546CB  mov      edx, 1
003546D0  cmp      dword ptr [rax + 0x28], ecx
003546D3  setne    cl
003546D6  add      ecx, 2
003546D9  add      rsp, 0x28
003546DD  jmp      0x3df7b0  ; -> 003DF7B0 fn
```

## 00354B00 (31 B, extent 00354B00-00354B1F)

Documented callee on this page: `002640C0`

```
00354B00  sub      rsp, 0x28
00354B04  call     0x2640c0  ; -> 002640C0 fn
00354B09  xor      ecx, ecx
00354B0B  cmp      dword ptr [rax + 0x28], ecx
00354B0E  setne    cl
00354B11  xor      edx, edx
00354B13  add      ecx, 2
00354B16  add      rsp, 0x28
00354B1A  jmp      0x3df7b0  ; -> 003DF7B0 fn
```

## 00355D90 (62 B, extent 00355D90-00355DCE)

Documented callee on this page: `002E1C70`

```
00355D90  mov      qword ptr [rsp + 8], rbx
00355D95  push     rdi
00355D96  sub      rsp, 0x20
00355D9A  mov      rcx, r9
00355D9D  mov      rdi, r9
00355DA0  call     0x267e10  ; -> 00267E10 fn
00355DA5  mov      rcx, rdi
00355DA8  mov      ebx, eax
00355DAA  call     0x267e10  ; -> 00267E10 fn
00355DAF  mov      edx, ebx
00355DB1  mov      ecx, eax
00355DB3  call     0x2e1c40  ; -> 002E1C40 fn
00355DB8  mov      edx, ebx
00355DBA  mov      ecx, 1
00355DBF  mov      rbx, qword ptr [rsp + 0x30]
00355DC4  add      rsp, 0x20
00355DC8  pop      rdi
00355DC9  jmp      0x2e1c70  ; -> 002E1C70 fn
```

## 00356080 (35 B, extent 00356080-003560A3)

Documented callee on this page: `002E1C70`

```
00356080  sub      rsp, 0x28
00356084  mov      rcx, r9
00356087  call     0x267e10  ; -> 00267E10 fn
0035608C  xor      edx, edx
0035608E  mov      ecx, eax
00356090  call     0x2e1c40  ; -> 002E1C40 fn
00356095  xor      edx, edx
00356097  lea      ecx, [rdx + 1]
0035609A  add      rsp, 0x28
0035609E  jmp      0x2e1c70  ; -> 002E1C70 fn
```

## 003562B0 (154 B, extent 003562B0-0035634A)

Documented callee on this page: `0026AF80`

```
003562B0  mov      qword ptr [rsp + 8], rbx
003562B5  push     rdi
003562B6  sub      rsp, 0x50
003562BA  movaps   xmmword ptr [rsp + 0x40], xmm6
003562BF  mov      rcx, r9
003562C2  movaps   xmmword ptr [rsp + 0x30], xmm7
003562C7  mov      rbx, r9
003562CA  mov      rdi, rdx
003562CD  call     0x267db0  ; -> 00267DB0 fn
003562D2  mov      rcx, rbx
003562D5  movaps   xmm6, xmm0
003562D8  call     0x267db0  ; -> 00267DB0 fn
003562DD  lea      r9, [rsp + 0x24]
003562E2  mov      rcx, rdi
003562E5  lea      r8, [rsp + 0x28]
003562EA  movaps   xmm7, xmm0
003562ED  lea      rdx, [rsp + 0x20]
003562F2  call     0x265020  ; -> 00265020 fn
003562F7  movss    xmm1, dword ptr [rsp + 0x20]
003562FD  mov      rcx, rdi
00356300  movss    xmm3, dword ptr [rsp + 0x24]
00356306  divss    xmm6, dword ptr [rip + 0x5a0a46]  ; -> 008F6D54 [f32 60]
0035630E  divss    xmm7, dword ptr [rip + 0x5a0a3e]  ; -> 008F6D54 [f32 60]
00356316  movss    xmm2, dword ptr [rsp + 0x28]
0035631C  subss    xmm1, xmm6
00356320  subss    xmm3, xmm7
00356324  movss    dword ptr [rsp + 0x20], xmm1
0035632A  movss    dword ptr [rsp + 0x24], xmm3
00356330  call     0x26af80  ; -> 0026AF80 fn
00356335  mov      rbx, qword ptr [rsp + 0x60]
0035633A  movaps   xmm6, xmmword ptr [rsp + 0x40]
0035633F  movaps   xmm7, xmmword ptr [rsp + 0x30]
00356344  add      rsp, 0x50
00356348  pop      rdi
00356349  ret      
```

## 003563D0 (109 B, extent 003563D0-0035643D)

Documented callee on this page: `002E1C70`

```
003563D0  mov      qword ptr [rsp + 8], rbx
003563D5  push     rdi
003563D6  sub      rsp, 0x20
003563DA  movzx    ecx, byte ptr [rdx + 0x15]
003563DE  mov      rdi, r9
003563E1  call     0x267310  ; -> 00267310 fn
003563E6  mov      rcx, rdi
003563E9  test     eax, eax
003563EB  je       0x35641b  ; -> 0035641B
003563ED  call     0x267e10  ; -> 00267E10 fn
003563F2  mov      rcx, rdi
003563F5  mov      ebx, eax
003563F7  call     0x267e10  ; -> 00267E10 fn
003563FC  mov      edx, ebx
003563FE  mov      ecx, eax
00356400  call     0x2e1c40  ; -> 002E1C40 fn
00356405  mov      edx, ebx
00356407  mov      ecx, 1
0035640C  mov      rbx, qword ptr [rsp + 0x30]
00356411  add      rsp, 0x20
00356415  pop      rdi
00356416  jmp      0x2e1c70  ; -> 002E1C70 fn
0035641B  call     0x267e10  ; -> 00267E10 fn
00356420  mov      rcx, rdi
00356423  mov      ebx, eax
00356425  call     0x267e10  ; -> 00267E10 fn
0035642A  mov      edx, ebx
0035642C  mov      ecx, eax
0035642E  mov      rbx, qword ptr [rsp + 0x30]
00356433  add      rsp, 0x20
00356437  pop      rdi
00356438  jmp      0x2e1c40  ; -> 002E1C40 fn
```

## 003567D0 (32 B, extent 003567D0-003567F0)

Documented callee on this page: `0026C120`

```
003567D0  push     rbx
003567D2  sub      rsp, 0x20
003567D6  mov      rbx, rdx
003567D9  call     0x357a20  ; -> 00357A20 fn
003567DE  mov      edx, 2
003567E3  mov      rcx, rbx
003567E6  add      rsp, 0x20
003567EA  pop      rbx
003567EB  jmp      0x26c120  ; -> 0026C120 fn
```

## 00356990 (73 B, extent 00356990-003569D9)

Documented callee on this page: `002E1C70`

```
00356990  push     rbx
00356992  sub      rsp, 0x20
00356996  movzx    ecx, byte ptr [rdx + 0x15]
0035699A  mov      rbx, r9
0035699D  call     0x267310  ; -> 00267310 fn
003569A2  mov      rcx, rbx
003569A5  test     eax, eax
003569A7  je       0x3569c6  ; -> 003569C6
003569A9  call     0x267e10  ; -> 00267E10 fn
003569AE  xor      edx, edx
003569B0  mov      ecx, eax
003569B2  call     0x2e1c40  ; -> 002E1C40 fn
003569B7  xor      edx, edx
003569B9  lea      ecx, [rdx + 1]
003569BC  add      rsp, 0x20
003569C0  pop      rbx
003569C1  jmp      0x2e1c70  ; -> 002E1C70 fn
003569C6  call     0x267e10  ; -> 00267E10 fn
003569CB  xor      edx, edx
003569CD  mov      ecx, eax
003569CF  add      rsp, 0x20
003569D3  pop      rbx
003569D4  jmp      0x2e1c40  ; -> 002E1C40 fn
```

## 00377560 (101 B, extent 00377560-003775C5)

Documented callee on this page: `0026AF80`

```
00377560  sub      rsp, 0x28
00377564  test     ecx, ecx
00377566  js       0x3775c0  ; -> 003775C0
00377568  call     0x2637b0  ; -> 002637B0 fn
0037756D  test     eax, eax
0037756F  js       0x3775c0  ; -> 003775C0
00377571  mov      edx, eax
00377573  xor      ecx, ecx
00377575  call     0x3587c0  ; -> 003587C0 fn
0037757A  test     rax, rax
0037757D  je       0x3775c0  ; -> 003775C0
0037757F  cmp      dword ptr [rip + 0x2765b52], 0  ; -> 02ADD0D8
00377586  xorps    xmm2, xmm2
00377589  movaps   xmm1, xmm2
0037758C  movaps   xmm3, xmm2
0037758F  je       0x3775b4  ; -> 003775B4
00377591  cmp      qword ptr [rip + 0x1d230d7], 0  ; -> 0209A670
00377599  je       0x3775b4  ; -> 003775B4
0037759B  mov      rcx, qword ptr [rip + 0x1d230d6]  ; -> 0209A678
003775A2  mov      rdx, qword ptr [rcx]
003775A5  test     rdx, rdx
003775A8  je       0x3775b4  ; -> 003775B4
003775AA  movss    xmm1, dword ptr [rdx + 0x28]
003775AF  movss    xmm3, dword ptr [rdx + 0x2c]
003775B4  mov      rcx, rax
003775B7  add      rsp, 0x28
003775BB  jmp      0x26af80  ; -> 0026AF80 fn
003775C0  add      rsp, 0x28
003775C4  ret      
```
