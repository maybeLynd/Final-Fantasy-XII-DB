# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 001D99C0 (125 B, extent 001D99C0-001D9A3D)

Documented callee on this page: `00210EB0`

```
001D99C0  mov      qword ptr [rsp + 0x18], rbp
001D99C5  push     rdi
001D99C6  sub      rsp, 0x20
001D99CA  lea      rdi, [rcx + 0x60]
001D99CE  mov      rbp, rcx
001D99D1  cmp      qword ptr [rdi], rdi
001D99D4  je       0x1d9a32  ; -> 001D9A32
001D99D6  mov      qword ptr [rsp + 0x30], rbx
001D99DB  mov      rbx, qword ptr [rdi]
001D99DE  cmp      rbx, rdi
001D99E1  je       0x1d99f4  ; -> 001D99F4
001D99E3  mov      rcx, qword ptr [rbx + 0x10]
001D99E7  call     0x210eb0  ; -> 00210EB0 fn
001D99EC  mov      rbx, qword ptr [rbx]
001D99EF  cmp      rbx, rdi
001D99F2  jne      0x1d99e3  ; -> 001D99E3
001D99F4  mov      rbx, qword ptr [rdi]
001D99F7  cmp      rbx, rdi
001D99FA  je       0x1d9a22  ; -> 001D9A22
001D99FC  mov      qword ptr [rsp + 0x38], rsi
001D9A01  mov      rax, qword ptr [rdi + 0x10]
001D9A05  lea      rcx, [rdi + 0x10]
001D9A09  mov      rdx, rbx
001D9A0C  mov      r8d, 0x18
001D9A12  mov      rbx, qword ptr [rbx]
001D9A15  call     qword ptr [rax + 0x18]
001D9A18  cmp      rbx, rdi
001D9A1B  jne      0x1d9a01  ; -> 001D9A01
001D9A1D  mov      rsi, qword ptr [rsp + 0x38]
001D9A22  mov      rbx, qword ptr [rsp + 0x30]
001D9A27  mov      qword ptr [rdi], rdi
001D9A2A  mov      qword ptr [rdi + 8], rdi
001D9A2E  mov      byte ptr [rbp + 0x78], 1
001D9A32  mov      rbp, qword ptr [rsp + 0x40]
001D9A37  add      rsp, 0x20
001D9A3B  pop      rdi
001D9A3C  ret      
```

## 001D9DA0 (273 B, extent 001D9DA0-001D9EB1)

Documented callee on this page: `005CD4F0`

```
001D9DA0  mov      qword ptr [rsp + 0x18], rbx
001D9DA5  mov      qword ptr [rsp + 0x20], rbp
001D9DAA  push     rsi
001D9DAB  push     rdi
001D9DAC  push     r14
001D9DAE  sub      rsp, 0x150
001D9DB5  mov      rax, qword ptr [rip + 0x1d6aa74]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001D9DBC  xor      rax, rsp
001D9DBF  mov      qword ptr [rsp + 0x140], rax
001D9DC7  mov      rsi, rcx
001D9DCA  mov      ebx, edx
001D9DCC  add      rcx, 0xf0
001D9DD3  call     0x5cd4f0  ; -> 005CD4F0 fn
001D9DD8  mov      r8d, ebx
001D9DDB  lea      rdx, [rip + 0x726976]  ; -> 00900758
001D9DE2  xor      ecx, ecx
001D9DE4  call     0x5cdaa0  ; -> 005CDAA0 fn
001D9DE9  xor      edx, edx
001D9DEB  lea      rcx, [rsp + 0x40]
001D9DF0  mov      r8d, 0x100
001D9DF6  call     0x861ec0  ; -> 00861EC0 fn
001D9DFB  lea      r14, [rip + 0x7268b6]  ; -> 009006B8 [str ".txt"]
001D9E02  mov      qword ptr [rsp + 0x30], r14
001D9E07  lea      rbp, [rip + 0x72697a]  ; -> 00900788 [str "/Events/"]
001D9E0E  mov      dword ptr [rsp + 0x28], ebx
001D9E12  lea      r9, [rsi + 0x1b8]
001D9E19  lea      r8, [rip + 0x726828]  ; -> 00900648 [str "/PrefetchData/"]
001D9E20  mov      qword ptr [rsp + 0x20], rbp
001D9E25  lea      rdx, [rip + 0x72696c]  ; -> 00900798 [str "%s%s%s%d%s"]
001D9E2C  lea      rcx, [rsp + 0x40]
001D9E31  call     0x17d2e0  ; -> 0017D2E0 fn
001D9E36  lea      rdx, [rsp + 0x40]
001D9E3B  mov      rcx, rsi
001D9E3E  call     0x1da9e0  ; -> 001DA9E0 fn
001D9E43  mov      qword ptr [rsp + 0x30], r14
001D9E48  lea      r9, [rip + 0x726959]  ; -> 009007A8 [str "/add-on/"]
001D9E4F  mov      dword ptr [rsp + 0x28], ebx
001D9E53  lea      r8, [rip + 0x7267ee]  ; -> 00900648 [str "/PrefetchData/"]
001D9E5A  lea      rdx, [rip + 0x726937]  ; -> 00900798 [str "%s%s%s%d%s"]
001D9E61  mov      qword ptr [rsp + 0x20], rbp
001D9E66  lea      rcx, [rsp + 0x40]
001D9E6B  call     0x17d2e0  ; -> 0017D2E0 fn
001D9E70  lea      rdx, [rsp + 0x40]
001D9E75  mov      rcx, rsi
001D9E78  call     0x1da9e0  ; -> 001DA9E0 fn
001D9E7D  lea      rcx, [rsi + 0xf0]
001D9E84  call     0x5cd820  ; -> 005CD820 fn
001D9E89  mov      rcx, qword ptr [rsp + 0x140]
001D9E91  xor      rcx, rsp
001D9E94  call     0x808c40  ; -> 00808C40 fn
001D9E99  lea      r11, [rsp + 0x150]
001D9EA1  mov      rbx, qword ptr [r11 + 0x30]
001D9EA5  mov      rbp, qword ptr [r11 + 0x38]
001D9EA9  mov      rsp, r11
001D9EAC  pop      r14
001D9EAE  pop      rdi
001D9EAF  pop      rsi
001D9EB0  ret      
```

## 001D9FD0 (169 B, extent 001D9FD0-001DA079)

Documented callee on this page: `005CD4F0`

```
001D9FD0  push     rbx
001D9FD2  sub      rsp, 0x20
001D9FD6  mov      rbx, rcx
001D9FD9  xor      ecx, ecx
001D9FDB  test     rdx, rdx
001D9FDE  sete     cl
001D9FE1  call     0x16d6a0  ; -> 0016D6A0 fn
001D9FE6  cmp      qword ptr [rbx + 0x30], 0
001D9FEB  je       0x1da073  ; -> 001DA073
001D9FF1  mov      qword ptr [rsp + 0x30], rsi
001D9FF6  lea      rcx, [rbx + 0x38]
001D9FFA  mov      qword ptr [rsp + 0x38], rdi
001D9FFF  call     0x5cd4f0  ; -> 005CD4F0 fn
001DA004  lea      rdi, [rbx + 0x60]
001DA008  cmp      qword ptr [rdi], rdi
001DA00B  je       0x1da023  ; -> 001DA023
001DA00D  lea      rdx, [rip + 0x7266ac]  ; -> 009006C0
001DA014  xor      ecx, ecx
001DA016  call     0x5cdaa0  ; -> 005CDAA0 fn
001DA01B  mov      rcx, rbx
001DA01E  call     0x1d99c0  ; -> 001D99C0 fn
001DA023  mov      rdx, qword ptr [rbx + 0x30]
001DA027  mov      r8, rdi
001DA02A  mov      rcx, rbx
001DA02D  call     0x1da0f0  ; -> 001DA0F0 fn
001DA032  test     al, al
001DA034  je       0x1da04f  ; -> 001DA04F
001DA036  cmp      qword ptr [rdi], rdi
001DA039  jne      0x1da04b  ; -> 001DA04B
001DA03B  lea      rdx, [rip + 0x72667e]  ; -> 009006C0
001DA042  xor      ecx, ecx
001DA044  call     0x5cdaa0  ; -> 005CDAA0 fn
001DA049  jmp      0x1da04f  ; -> 001DA04F
001DA04B  mov      byte ptr [rbx + 0x78], 0
001DA04F  lea      rcx, [rbx + 0x38]
001DA053  call     0x5cd820  ; -> 005CD820 fn
001DA058  mov      rcx, qword ptr [rbx + 0x30]
001DA05C  call     0x210eb0  ; -> 00210EB0 fn
001DA061  mov      rdi, qword ptr [rsp + 0x38]
001DA066  mov      rsi, qword ptr [rsp + 0x30]
001DA06B  mov      qword ptr [rbx + 0x30], 0
001DA073  add      rsp, 0x20
001DA077  pop      rbx
001DA078  ret      
```

## 001DCEB0 (402 B, extent 001DCEB0-001DD042)

Documented callee on this page: `00808C40`

```
001DCEB0  mov      r11, rsp
001DCEB3  mov      qword ptr [r11 + 8], rbx
001DCEB7  mov      qword ptr [r11 + 0x10], rbp
001DCEBB  mov      qword ptr [r11 + 0x18], rsi
001DCEBF  mov      qword ptr [r11 + 0x20], rdi
001DCEC3  push     r13
001DCEC5  push     r14
001DCEC7  push     r15
001DCEC9  sub      rsp, 0x40
001DCECD  mov      rax, qword ptr [rip + 0x1d6795c]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001DCED4  xor      rax, rsp
001DCED7  mov      qword ptr [rsp + 0x30], rax
001DCEDC  mov      rdi, rcx
001DCEDF  mov      qword ptr [r11 - 0x38], 0
001DCEE7  lea      rcx, [r11 - 0x38]
001DCEEB  mov      qword ptr [r11 - 0x30], 0
001DCEF3  xor      r8d, r8d
001DCEF6  mov      edx, 0xcf0000
001DCEFB  call     qword ptr [rip + 0x6e5ac7]  ; -> 008C29C8 [u64 0x0000000001CCC84E]
001DCF01  mov      rax, qword ptr [rip + 0x1da5e18]  ; -> 01F82D20
001DCF08  xor      r9d, r9d
001DCF0B  mov      r15d, dword ptr [rdi + 0x50]
001DCF0F  xor      ebp, ebp
001DCF11  mov      r11d, dword ptr [rax + 0x74]
001DCF15  mov      ebx, dword ptr [rax + 0x78]
001DCF18  test     r15d, r15d
001DCF1B  je       0x1dd00d  ; -> 001DD00D
001DCF21  mov      r13, qword ptr [rdi + 0x78]
001DCF25  xor      r14d, r14d
001DCF28  lea      rsi, [r13 + 0x130]
001DCF2F  nop      
001DCF30  mov      edi, dword ptr [rsi]
001DCF32  xor      r10d, r10d
001DCF35  test     edi, edi
001DCF37  je       0x1dcff4  ; -> 001DCFF4
001DCF3D  mov      rcx, qword ptr [r14 + r13 + 0x138]
001DCF45  add      rcx, 0x4c
001DCF49  nop      dword ptr [rax]
001DCF50  mov      edx, dword ptr [rcx - 0xc]
001DCF53  cmp      r11d, edx
001DCF56  jl       0x1dcf6b  ; -> 001DCF6B
001DCF58  cmp      r11d, dword ptr [rcx - 4]
001DCF5C  jge      0x1dcf6b  ; -> 001DCF6B
001DCF5E  cmp      ebx, dword ptr [rcx - 8]
001DCF61  jl       0x1dcf6b  ; -> 001DCF6B
001DCF63  cmp      ebx, dword ptr [rcx]
001DCF65  jl       0x1dd03c  ; -> 001DD03C
001DCF6B  test     r9, r9
001DCF6E  je       0x1dcfe0  ; -> 001DCFE0
001DCF70  mov      eax, dword ptr [rcx - 4]
001DCF73  add      eax, edx
001DCF75  cdq      
001DCF76  sub      eax, edx
001DCF78  sar      eax, 1
001DCF7A  sub      eax, r11d
001DCF7D  movd     xmm3, eax
001DCF81  mov      eax, dword ptr [rcx - 8]
001DCF84  add      eax, dword ptr [rcx]
001DCF86  cdq      
001DCF87  sub      eax, edx
001DCF89  sar      eax, 1
001DCF8B  sub      eax, ebx
001DCF8D  cvtdq2ps xmm3, xmm3
001DCF90  movd     xmm2, eax
001DCF94  mov      eax, dword ptr [r9 + 8]
001DCF98  add      eax, dword ptr [r9]
001DCF9B  cdq      
001DCF9C  mulss    xmm3, xmm3
001DCFA0  sub      eax, edx
001DCFA2  sar      eax, 1
001DCFA4  sub      eax, r11d
001DCFA7  cvtdq2ps xmm2, xmm2
001DCFAA  movd     xmm1, eax
001DCFAE  mov      eax, dword ptr [r9 + 0xc]
001DCFB2  add      eax, dword ptr [r9 + 4]
001DCFB6  cdq      
001DCFB7  mulss    xmm2, xmm2
001DCFBB  sub      eax, edx
001DCFBD  sar      eax, 1
001DCFBF  sub      eax, ebx
001DCFC1  cvtdq2ps xmm1, xmm1
001DCFC4  movd     xmm0, eax
001DCFC8  addss    xmm2, xmm3
001DCFCC  cvtdq2ps xmm0, xmm0
001DCFCF  mulss    xmm1, xmm1
001DCFD3  mulss    xmm0, xmm0
001DCFD7  addss    xmm0, xmm1
001DCFDB  comiss   xmm0, xmm2
001DCFDE  jbe      0x1dcfe4  ; -> 001DCFE4
001DCFE0  lea      r9, [rcx - 0xc]
001DCFE4  inc      r10d
001DCFE7  add      rcx, 0x60
001DCFEB  cmp      r10d, edi
001DCFEE  jb       0x1dcf50  ; -> 001DCF50
001DCFF4  inc      ebp
001DCFF6  add      r14, 0x140
001DCFFD  add      rsi, 0x140
001DD004  cmp      ebp, r15d
001DD007  jb       0x1dcf30  ; -> 001DCF30
001DD00D  mov      rax, r9
001DD010  mov      rcx, qword ptr [rsp + 0x30]
001DD015  xor      rcx, rsp
001DD018  call     0x808c40  ; -> 00808C40 fn
001DD01D  mov      rbx, qword ptr [rsp + 0x60]
001DD022  mov      rbp, qword ptr [rsp + 0x68]
001DD027  mov      rsi, qword ptr [rsp + 0x70]
001DD02C  mov      rdi, qword ptr [rsp + 0x78]
001DD031  add      rsp, 0x40
001DD035  pop      r15
001DD037  pop      r14
001DD039  pop      r13
001DD03B  ret      
001DD03C  lea      rax, [rcx - 0xc]
001DD040  jmp      0x1dd010  ; -> 001DD010
```

## 001E74F0 (96 B, extent 001E74F0-001E7550)

Documented callee on this page: `005CD6D0`

```
001E74F0  push     rbx
001E74F2  sub      rsp, 0x30
001E74F6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001E74FF  mov      rbx, rcx
001E7502  cmp      byte ptr [rcx + 0xb8], 0
001E7509  je       0x1e7518  ; -> 001E7518
001E750B  add      rcx, 0x90
001E7512  call     0x5cd6d0  ; -> 005CD6D0 fn
001E7517  nop      
001E7518  lea      rcx, [rbx + 0x58]
001E751C  call     0x1e7560  ; -> 001E7560 fn
001E7521  nop      
001E7522  lea      rcx, [rbx + 0x20]
001E7526  call     0x1e7560  ; -> 001E7560 fn
001E752B  nop      
001E752C  mov      rdx, qword ptr [rbx]
001E752F  test     rdx, rdx
001E7532  je       0x1e754a  ; -> 001E754A
001E7534  lea      rcx, [rbx + 0x18]
001E7538  mov      rax, qword ptr [rcx]
001E753B  mov      r8, qword ptr [rbx + 0x10]
001E753F  sub      r8, rdx
001E7542  and      r8, 0xfffffffffffffff0
001E7546  call     qword ptr [rax + 0x18]
001E7549  nop      
001E754A  add      rsp, 0x30
001E754E  pop      rbx
001E754F  ret      
```

## 001EA130 (69 B, extent 001EA130-001EA175)

Documented callee on this page: `00584730`

```
001EA130  push     rbx
001EA132  sub      rsp, 0x30
001EA136  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001EA13F  mov      rbx, rcx
001EA142  mov      ecx, dword ptr [rcx]
001EA144  mov      eax, ecx
001EA146  shr      eax, 0x1f
001EA149  not      al
001EA14B  test     al, 1
001EA14D  je       0x1ea167  ; -> 001EA167
001EA14F  btr      ecx, 0x1f
001EA153  cmp      ecx, 1
001EA156  jbe      0x1ea167  ; -> 001EA167
001EA158  mov      rcx, qword ptr [rbx + 8]
001EA15C  test     rcx, rcx
001EA15F  je       0x1ea167  ; -> 001EA167
001EA161  call     0x584730  ; -> 00584730 fn
001EA166  nop      
001EA167  xor      eax, eax
001EA169  mov      qword ptr [rbx + 8], rax
001EA16D  mov      dword ptr [rbx], eax
001EA16F  add      rsp, 0x30
001EA173  pop      rbx
001EA174  ret      
```

## 001EBAE0 (71 B, extent 001EBAE0-001EBB27)

Documented callee on this page: `00808C40`

```
001EBAE0  test     rdx, rdx
001EBAE3  je       0x1ebb26  ; -> 001EBB26
001EBAE5  sub      rsp, 0x48
001EBAE9  mov      rax, qword ptr [rip + 0x1d58d40]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001EBAF0  xor      rax, rsp
001EBAF3  mov      qword ptr [rsp + 0x30], rax
001EBAF8  mov      rax, qword ptr [rdx]
001EBAFB  mov      r8, rdx
001EBAFE  movaps   xmm0, xmmword ptr [rip + 0x71694b]  ; -> 00902450 [f32x4 255, 255, 255, 255]
001EBB05  lea      rdx, [rsp + 0x20]
001EBB0A  mov      rcx, r8
001EBB0D  movups   xmmword ptr [rsp + 0x20], xmm0
001EBB12  call     qword ptr [rax + 0x48]
001EBB15  mov      rcx, qword ptr [rsp + 0x30]
001EBB1A  xor      rcx, rsp
001EBB1D  call     0x808c40  ; -> 00808C40 fn
001EBB22  add      rsp, 0x48
001EBB26  ret      
```

## 001FD9A0 (189 B, extent 001FD9A0-001FDA5D)

Documented callee on this page: `00220390`

```
001FD9A0  test     rdx, rdx
001FD9A3  je       0x1fda5c  ; -> 001FDA5C
001FD9A9  mov      qword ptr [rsp + 0x10], rdx
001FD9AE  mov      qword ptr [rsp + 8], rcx
001FD9B3  push     rbp
001FD9B4  push     rsi
001FD9B5  push     rdi
001FD9B6  sub      rsp, 0x30
001FD9BA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001FD9C3  mov      qword ptr [rsp + 0x68], rbx
001FD9C8  mov      rbp, rdx
001FD9CB  nop      dword ptr [rax + rax]
001FD9D0  mov      rdx, qword ptr [rbp]
001FD9D4  call     0x1fd9a0  ; -> 001FD9A0 fn
001FD9D9  mov      rdi, qword ptr [rbp + 8]
001FD9DD  mov      qword ptr [rsp + 0x60], rdi
001FD9E2  mov      rbx, qword ptr [rbp + 0x40]
001FD9E6  test     rbx, rbx
001FD9E9  je       0x1fda26  ; -> 001FDA26
001FD9EB  nop      dword ptr [rax + rax]
001FD9F0  mov      rdx, qword ptr [rbx]
001FD9F3  lea      rcx, [rbp + 0x28]
001FD9F7  call     0x220390  ; -> 00220390 fn
001FD9FC  mov      rdi, qword ptr [rbx + 8]
001FDA00  mov      rax, qword ptr [rbp + 0x58]
001FDA04  mov      r8d, 0x28
001FDA0A  mov      rdx, rbx
001FDA0D  lea      rcx, [rbp + 0x58]
001FDA11  call     qword ptr [rax + 0x18]
001FDA14  mov      rbx, rdi
001FDA17  test     rdi, rdi
001FDA1A  jne      0x1fd9f0  ; -> 001FD9F0
001FDA1C  mov      rbp, qword ptr [rsp + 0x58]
001FDA21  mov      rdi, qword ptr [rsp + 0x60]
001FDA26  mov      rcx, qword ptr [rsp + 0x50]
001FDA2B  add      rcx, 0x30
001FDA2F  mov      rax, qword ptr [rcx]
001FDA32  mov      r8d, 0x60
001FDA38  mov      rdx, rbp
001FDA3B  call     qword ptr [rax + 0x18]
001FDA3E  mov      rbp, rdi
001FDA41  mov      qword ptr [rsp + 0x58], rdi
001FDA46  test     rdi, rdi
001FDA49  mov      rcx, qword ptr [rsp + 0x50]
001FDA4E  jne      0x1fd9d0  ; -> 001FD9D0
001FDA50  mov      rbx, qword ptr [rsp + 0x68]
001FDA55  add      rsp, 0x30
001FDA59  pop      rdi
001FDA5A  pop      rsi
001FDA5B  pop      rbp
001FDA5C  ret      
```

## 00204B30 (67 B, extent 00204B30-00204B73)

Documented callee on this page: `00809950`

```
00204B30  mov      qword ptr [rsp + 8], rbx
00204B35  push     rdi
00204B36  sub      rsp, 0x20
00204B3A  mov      rdi, rcx
00204B3D  mov      ebx, edx
00204B3F  mov      rcx, qword ptr [rcx + 0x28]
00204B43  call     qword ptr [rip + 0x6bdfff]  ; -> 008C2B48 [u64 0x0000000001CCEE80]
00204B49  lea      rax, [rip + 0x700d70]  ; -> 009058C0
00204B50  mov      qword ptr [rdi], rax
00204B53  test     bl, 1
00204B56  je       0x204b65  ; -> 00204B65
00204B58  mov      edx, 0x30
00204B5D  mov      rcx, rdi
00204B60  call     0x809950  ; -> 00809950 fn
00204B65  mov      rax, rdi
00204B68  mov      rbx, qword ptr [rsp + 0x30]
00204B6D  add      rsp, 0x20
00204B71  pop      rdi
00204B72  ret      
```

## 00204B80 (76 B, extent 00204B80-00204BCC)

Documented callee on this page: `00809950`

```
00204B80  mov      qword ptr [rsp + 8], rbx
00204B85  push     rdi
00204B86  sub      rsp, 0x20
00204B8A  lea      rax, [rip + 0x700cf7]  ; -> 00905888
00204B91  mov      rdi, rcx
00204B94  mov      qword ptr [rcx], rax
00204B97  mov      ebx, edx
00204B99  mov      rcx, qword ptr [rcx + 0x18]
00204B9D  call     qword ptr [rip + 0x6bdfa5]  ; -> 008C2B48 [u64 0x0000000001CCEE80]
00204BA3  mov      rcx, rdi
00204BA6  call     qword ptr [rip + 0x6bd8a4]  ; -> 008C2450 [u64 0x0000000001CCE672]
00204BAC  test     bl, 1
00204BAF  je       0x204bbe  ; -> 00204BBE
00204BB1  mov      edx, 0x20
00204BB6  mov      rcx, rdi
00204BB9  call     0x809950  ; -> 00809950 fn
00204BBE  mov      rax, rdi
00204BC1  mov      rbx, qword ptr [rsp + 0x30]
00204BC6  add      rsp, 0x20
00204BCA  pop      rdi
00204BCB  ret      
```

## 002093D0 (116 B, extent 002093D0-00209444)

Documented callee on this page: `00210EB0`

```
002093D0  push     rbx
002093D2  sub      rsp, 0x20
002093D6  mov      rbx, rcx
002093D9  mov      rcx, qword ptr [rcx]
002093DC  test     rcx, rcx
002093DF  je       0x20943e  ; -> 0020943E
002093E1  mov      rax, qword ptr [rbx + 0x10]
002093E5  sub      rax, rcx
002093E8  cmp      rax, 0x1000
002093EE  jb       0x20942c  ; -> 0020942C
002093F0  test     cl, 0x1f
002093F3  je       0x2093fc  ; -> 002093FC
002093F5  call     qword ptr [rip + 0x6b99ad]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
002093FB  int3     
002093FC  mov      rax, qword ptr [rcx - 8]
00209400  cmp      rax, rcx
00209403  jb       0x20940c  ; -> 0020940C
00209405  call     qword ptr [rip + 0x6b999d]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
0020940B  int3     
0020940C  sub      rcx, rax
0020940F  cmp      rcx, 8
00209413  jae      0x20941c  ; -> 0020941C
00209415  call     qword ptr [rip + 0x6b998d]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
0020941B  int3     
0020941C  cmp      rcx, 0x27
00209420  jbe      0x209429  ; -> 00209429
00209422  call     qword ptr [rip + 0x6b9980]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
00209428  int3     
00209429  mov      rcx, rax
0020942C  call     0x210eb0  ; -> 00210EB0 fn
00209431  xor      eax, eax
00209433  mov      qword ptr [rbx], rax
00209436  mov      qword ptr [rbx + 8], rax
0020943A  mov      qword ptr [rbx + 0x10], rax
0020943E  add      rsp, 0x20
00209442  pop      rbx
00209443  ret      
```

## 0020B3E0 (131 B, extent 0020B3E0-0020B463)

Documented callee on this page: `005CD6D0`

```
0020B3E0  push     rbx
0020B3E2  sub      rsp, 0x30
0020B3E6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0020B3EF  mov      rbx, rcx
0020B3F2  cmp      byte ptr [rcx + 0xb8], 0
0020B3F9  je       0x20b408  ; -> 0020B408
0020B3FB  add      rcx, 0x90
0020B402  call     0x5cd6d0  ; -> 005CD6D0 fn
0020B407  nop      
0020B408  lea      rcx, [rbx + 0x58]
0020B40C  call     0x20b500  ; -> 0020B500 fn
0020B411  nop      
0020B412  lea      rcx, [rbx + 0x20]
0020B416  call     0x20b500  ; -> 0020B500 fn
0020B41B  nop      
0020B41C  mov      r10, qword ptr [rbx]
0020B41F  test     r10, r10
0020B422  je       0x20b45d  ; -> 0020B45D
0020B424  lea      rcx, [rbx + 0x18]
0020B428  mov      r9, qword ptr [rcx]
0020B42B  mov      r8, qword ptr [rbx + 0x10]
0020B42F  sub      r8, r10
0020B432  movabs   rax, 0x2aaaaaaaaaaaaaab
0020B43C  imul     r8
0020B43F  sar      rdx, 2
0020B443  mov      rax, rdx
0020B446  shr      rax, 0x3f
0020B44A  add      rdx, rax
0020B44D  lea      r8, [rdx + rdx*2]
0020B451  shl      r8, 3
0020B455  mov      rdx, r10
0020B458  call     qword ptr [r9 + 0x18]
0020B45C  nop      
0020B45D  add      rsp, 0x30
0020B461  pop      rbx
0020B462  ret      
```

## 00220DA0 (52 B, extent 00220DA0-00220DD4)

Documented callee on this page: `0016D6A0`

```
00220DA0  mov      qword ptr [rsp + 8], rbx
00220DA5  push     rdi
00220DA6  sub      rsp, 0x20
00220DAA  mov      rdi, rcx
00220DAD  movsxd   rbx, edx
00220DB0  xor      ecx, ecx
00220DB2  cmp      ebx, 0xff
00220DB8  setbe    cl
00220DBB  call     0x16d6a0  ; -> 0016D6A0 fn
00220DC0  movss    xmm0, dword ptr [rdi + rbx*4 + 0x3d8]
00220DC9  mov      rbx, qword ptr [rsp + 0x30]
00220DCE  add      rsp, 0x20
00220DD2  pop      rdi
00220DD3  ret      
```

## 00221100 (51 B, extent 00221100-00221133)

Documented callee on this page: `0016D6A0`

```
00221100  mov      qword ptr [rsp + 8], rbx
00221105  push     rdi
00221106  sub      rsp, 0x20
0022110A  mov      rdi, rcx
0022110D  movsxd   rbx, edx
00221110  xor      ecx, ecx
00221112  cmp      ebx, 0xff
00221118  setbe    cl
0022111B  call     0x16d6a0  ; -> 0016D6A0 fn
00221120  movzx    eax, byte ptr [rbx + rdi + 0x7d8]
00221128  mov      rbx, qword ptr [rsp + 0x30]
0022112D  add      rsp, 0x20
00221131  pop      rdi
00221132  ret      
```

## 00221280 (134 B, extent 00221280-00221306)

Documented callee on this page: `0016D6A0`

```
00221280  mov      qword ptr [rsp + 8], rbx
00221285  mov      qword ptr [rsp + 0x10], rsi
0022128A  push     rdi
0022128B  sub      rsp, 0x20
0022128F  xor      ebx, ebx
00221291  movsxd   rsi, edx
00221294  mov      rdi, rcx
00221297  test     edx, edx
00221299  jns      0x2212d8  ; -> 002212D8
0022129B  mov      eax, ebx
0022129D  lea      rdx, [rcx + 0x3d8]
002212A4  nop      dword ptr [rax]
002212A8  nop      dword ptr [rax + rax]
002212B0  mov      dword ptr [rdx], ebx
002212B2  lea      rdx, [rdx + 4]
002212B6  mov      byte ptr [rcx + rax + 0x7d8], bl
002212BD  inc      rax
002212C0  cmp      rax, 0x100
002212C6  jl       0x2212b0  ; -> 002212B0
002212C8  mov      rbx, qword ptr [rsp + 0x30]
002212CD  mov      rsi, qword ptr [rsp + 0x38]
002212D2  add      rsp, 0x20
002212D6  pop      rdi
002212D7  ret      
002212D8  cmp      esi, 0x100
002212DE  mov      ecx, ebx
002212E0  setl     cl
002212E3  call     0x16d6a0  ; -> 0016D6A0 fn
002212E8  mov      dword ptr [rdi + rsi*4 + 0x3d8], ebx
002212EF  mov      byte ptr [rsi + rdi + 0x7d8], bl
002212F6  mov      rbx, qword ptr [rsp + 0x30]
002212FB  mov      rsi, qword ptr [rsp + 0x38]
00221300  add      rsp, 0x20
00221304  pop      rdi
00221305  ret      
```

## 00225B20 (117 B, extent 00225B20-00225B95)

Documented callee on this page: `00861EBA`

```
00225B20  sub      rsp, 0x28
00225B24  mov      r8d, dword ptr [rcx + 0x10]
00225B28  mov      r9, rdx
00225B2B  test     r8d, r8d
00225B2E  jle      0x225b8e  ; -> 00225B8E
00225B30  mov      r10, qword ptr [rcx + 8]
00225B34  test     r10, r10
00225B37  je       0x225b8e  ; -> 00225B8E
00225B39  movd     xmm1, dword ptr [rdx + 0x10]
00225B3E  movd     xmm0, dword ptr [rdx + 0x14]
00225B43  cvtdq2ps xmm1, xmm1
00225B46  cvtdq2ps xmm0, xmm0
00225B49  divss    xmm1, xmm0
00225B4D  comiss   xmm1, dword ptr [rip + 0x1ac601c]  ; -> 01CEBB70 [f32 0.5]
00225B54  ja       0x225b8e  ; -> 00225B8E
00225B56  movsxd   rax, dword ptr [rdx + 8]
00225B5A  movsxd   rcx, dword ptr [rdx + 0xc]
00225B5E  mov      qword ptr [rsp + 0x20], rbx
00225B63  mov      rbx, rax
00225B66  add      eax, ecx
00225B68  cmp      eax, r8d
00225B6B  jl       0x225b73  ; -> 00225B73
00225B6D  sub      r8d, ecx
00225B70  movsxd   rbx, r8d
00225B73  lea      rdx, [r10 + rcx]
00225B77  mov      r8, rbx
00225B7A  mov      rcx, qword ptr [r9]
00225B7D  call     0x861eba  ; -> 00861EBA fn
00225B82  mov      eax, ebx
00225B84  mov      rbx, qword ptr [rsp + 0x20]
00225B89  add      rsp, 0x28
00225B8D  ret      
00225B8E  xor      eax, eax
00225B90  add      rsp, 0x28
00225B94  ret      
```

## 00240A00 (86 B, extent 00240A00-00240A56)

Documented callee on this page: `00808C40`

```
00240A00  sub      rsp, 0x48
00240A04  mov      rax, qword ptr [rip + 0x1d03e25]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00240A0B  xor      rax, rsp
00240A0E  mov      qword ptr [rsp + 0x38], rax
00240A13  mov      rcx, qword ptr [rip + 0x1e4dca6]  ; -> 0208E6C0
00240A1A  test     rcx, rcx
00240A1D  je       0x240a44  ; -> 00240A44
00240A1F  movdqa   xmm0, xmmword ptr [rip + 0x6d4329]  ; -> 00914D50 [u32x4 0x00002CA6, 0x00000000, 0x00000005, 0x00000000]
00240A27  movdqu   xmmword ptr [rsp + 0x28], xmm0
00240A2D  mov      dword ptr [rsp + 0x20], 0xd
00240A35  mov      rax, qword ptr [rcx]
00240A38  test     rax, rax
00240A3B  je       0x240a44  ; -> 00240A44
00240A3D  lea      rdx, [rsp + 0x20]
00240A42  call     rax
00240A44  mov      rcx, qword ptr [rsp + 0x38]
00240A49  xor      rcx, rsp
00240A4C  call     0x808c40  ; -> 00808C40 fn
00240A51  add      rsp, 0x48
00240A55  ret      
```

## 0028E190 (51 B, extent 0028E190-0028E1C3)

Documented callee on this page: `0016D6A0`

```
0028E190  sub      rsp, 0x28
0028E194  mov      rcx, qword ptr [rip + 0x1e0dce5]  ; -> 0209BE80
0028E19B  add      rcx, 0x8fa0
0028E1A2  call     0x2bdae0  ; -> 002BDAE0 fn
0028E1A7  mov      rcx, qword ptr [rip + 0x1e0dcd2]  ; -> 0209BE80
0028E1AE  add      rcx, 0x8fa0
0028E1B5  call     0x16d6a0  ; -> 0016D6A0 fn
0028E1BA  add      rsp, 0x28
0028E1BE  jmp      0x3bbb30  ; -> 003BBB30 fn
```

## 002A7EA0 (21 B, extent 002A7EA0-002A7EB5)

Documented callee on this page: `0016D6A0`

```
002A7EA0  sub      rsp, 0x28
002A7EA4  mov      ecx, 0x1000
002A7EA9  call     0x16d6a0  ; -> 0016D6A0 fn
002A7EAE  xor      eax, eax
002A7EB0  add      rsp, 0x28
002A7EB4  ret      
```

## 002D5500 (144 B, extent 002D5500-002D5590)

Documented callee on this page: `00808C40`

```
002D5500  sub      rsp, 0x28
002D5504  mov      rax, qword ptr [rip + 0x1c6f325]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D550B  xor      rax, rsp
002D550E  mov      qword ptr [rsp + 0x10], rax
002D5513  mov      r10d, edx
002D5516  test     rcx, rcx
002D5519  jne      0x2d5520  ; -> 002D5520
002D551B  xor      r9d, r9d
002D551E  jmp      0x2d5528  ; -> 002D5528
002D5520  mov      rax, qword ptr [rcx + 0x60]
002D5524  mov      r9, qword ptr [rax + 0x10]
002D5528  mov      r9, qword ptr [r9 + 0x18]
002D552C  lea      r8, [rsp]
002D5530  mov      dword ptr [rsp], 0
002D5537  xor      edx, edx
002D5539  mov      dword ptr [rsp + 4], 1
002D5541  mov      dword ptr [rsp + 8], 2
002D5549  nop      dword ptr [rax]
002D5550  test     r9, r9
002D5553  jne      0x2d5559  ; -> 002D5559
002D5555  xor      ecx, ecx
002D5557  jmp      0x2d5564  ; -> 002D5564
002D5559  movsxd   rcx, dword ptr [r8]
002D555C  mov      rax, qword ptr [r9 + 0x60]
002D5560  mov      rcx, qword ptr [rax + rcx*8]
002D5564  and      dword ptr [rcx + 8], 0xfffffffe
002D5568  xor      eax, eax
002D556A  cmp      edx, r10d
002D556D  setl     al
002D5570  inc      edx
002D5572  or       dword ptr [rcx + 8], eax
002D5575  add      r8, 4
002D5579  cmp      edx, 3
002D557C  jb       0x2d5550  ; -> 002D5550
002D557E  mov      rcx, qword ptr [rsp + 0x10]
002D5583  xor      rcx, rsp
002D5586  call     0x808c40  ; -> 00808C40 fn
002D558B  add      rsp, 0x28
002D558F  ret      
```
