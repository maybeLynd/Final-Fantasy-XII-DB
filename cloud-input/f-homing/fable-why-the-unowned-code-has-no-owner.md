# F homing pack (FABLE): `99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 10. No bearing page cites them and no documented function calls them directly.

## 00237430 (46 B, extent 00237430-0023745E)

Documented callee on this page: `0031B760`

```
00237430  sub      rsp, 0x28
00237434  call     0x31b760  ; -> 0031B760 fn
00237439  test     rax, rax
0023743C  jne      0x237445  ; -> 00237445
0023743E  xor      eax, eax
00237440  add      rsp, 0x28
00237444  ret      
00237445  mov      rax, qword ptr [rax + 0x6a0]
0023744C  test     rax, rax
0023744F  je       0x23743e  ; -> 0023743E
00237451  mov      eax, dword ptr [rax]
00237453  shr      eax, 5
00237456  and      eax, 1
00237459  add      rsp, 0x28
0023745D  ret      
```

## 0031C1A0 (89 B, extent 0031C1A0-0031C1F9)

Documented callee on this page: `00263E30`

```
0031C1A0  mov      qword ptr [rsp + 8], rbx
0031C1A5  push     rdi
0031C1A6  sub      rsp, 0x20
0031C1AA  movsxd   rbx, edx
0031C1AD  mov      rdi, r8
0031C1B0  test     rcx, rcx
0031C1B3  je       0x31c1eb  ; -> 0031C1EB
0031C1B5  call     0x263e30  ; -> 00263E30 fn
0031C1BA  test     rax, rax
0031C1BD  je       0x31c1eb  ; -> 0031C1EB
0031C1BF  cmp      ebx, 0xf
0031C1C2  ja       0x31c1db  ; -> 0031C1DB
0031C1C4  movzx    eax, byte ptr [rbx + rax + 0xec0]
0031C1CC  mov      byte ptr [rdi], al
0031C1CE  xor      eax, eax
0031C1D0  mov      rbx, qword ptr [rsp + 0x30]
0031C1D5  add      rsp, 0x20
0031C1D9  pop      rdi
0031C1DA  ret      
0031C1DB  mov      eax, 0xfffffffe
0031C1E0  mov      rbx, qword ptr [rsp + 0x30]
0031C1E5  add      rsp, 0x20
0031C1E9  pop      rdi
0031C1EA  ret      
0031C1EB  or       eax, 0xffffffff
0031C1EE  mov      rbx, qword ptr [rsp + 0x30]
0031C1F3  add      rsp, 0x20
0031C1F7  pop      rdi
0031C1F8  ret      
```

## 00329020 (88 B, extent 00329020-00329078)

Documented callee on this page: `00263E30`

```
00329020  mov      qword ptr [rsp + 8], rbx
00329025  push     rdi
00329026  sub      rsp, 0x20
0032902A  movsxd   rbx, edx
0032902D  movzx    edi, r8b
00329031  test     rcx, rcx
00329034  je       0x32906a  ; -> 0032906A
00329036  call     0x263e30  ; -> 00263E30 fn
0032903B  test     rax, rax
0032903E  je       0x32906a  ; -> 0032906A
00329040  cmp      ebx, 0xf
00329043  ja       0x32905a  ; -> 0032905A
00329045  mov      byte ptr [rbx + rax + 0xec0], dil
0032904D  xor      eax, eax
0032904F  mov      rbx, qword ptr [rsp + 0x30]
00329054  add      rsp, 0x20
00329058  pop      rdi
00329059  ret      
0032905A  mov      eax, 0xfffffffe
0032905F  mov      rbx, qword ptr [rsp + 0x30]
00329064  add      rsp, 0x20
00329068  pop      rdi
00329069  ret      
0032906A  or       eax, 0xffffffff
0032906D  mov      rbx, qword ptr [rsp + 0x30]
00329072  add      rsp, 0x20
00329076  pop      rdi
00329077  ret      
```

## 004736E0 (37 B, extent 004736E0-00473705)

Documented callee on this page: `003206E0`

```
004736E0  sub      rsp, 0x28
004736E4  test     rcx, rcx
004736E7  je       0x4736fe  ; -> 004736FE
004736E9  call     0x3589b0  ; -> 003589B0 fn
004736EE  xor      r8d, r8d
004736F1  xor      edx, edx
004736F3  mov      ecx, eax
004736F5  add      rsp, 0x28
004736F9  jmp      0x3206e0  ; -> 003206E0 fn
004736FE  xor      eax, eax
00473700  add      rsp, 0x28
00473704  ret      
```

## 00473710 (38 B, extent 00473710-00473736)

Documented callee on this page: `003206E0`

```
00473710  sub      rsp, 0x28
00473714  test     rcx, rcx
00473717  je       0x47372f  ; -> 0047372F
00473719  call     0x3589b0  ; -> 003589B0 fn
0047371E  xor      edx, edx
00473720  mov      ecx, eax
00473722  lea      r8d, [rdx + 0x64]
00473726  add      rsp, 0x28
0047372A  jmp      0x3206e0  ; -> 003206E0 fn
0047372F  xor      eax, eax
00473731  add      rsp, 0x28
00473735  ret      
```

## 00473740 (39 B, extent 00473740-00473767)

Documented callee on this page: `003206E0`

```
00473740  sub      rsp, 0x28
00473744  test     rcx, rcx
00473747  je       0x473760  ; -> 00473760
00473749  call     0x3589b0  ; -> 003589B0 fn
0047374E  xor      r8d, r8d
00473751  mov      ecx, eax
00473753  lea      edx, [r8 + 1]
00473757  add      rsp, 0x28
0047375B  jmp      0x3206e0  ; -> 003206E0 fn
00473760  xor      eax, eax
00473762  add      rsp, 0x28
00473766  ret      
```

## 00473770 (41 B, extent 00473770-00473799)

Documented callee on this page: `003206E0`

```
00473770  sub      rsp, 0x28
00473774  test     rcx, rcx
00473777  je       0x473792  ; -> 00473792
00473779  call     0x3589b0  ; -> 003589B0 fn
0047377E  mov      edx, 1
00473783  mov      ecx, eax
00473785  lea      r8d, [rdx + 0x63]
00473789  add      rsp, 0x28
0047378D  jmp      0x3206e0  ; -> 003206E0 fn
00473792  xor      eax, eax
00473794  add      rsp, 0x28
00473798  ret      
```

## 004737A0 (46 B, extent 004737A0-004737CE)

Documented callee on this page: `003206E0`

```
004737A0  push     rbx
004737A2  sub      rsp, 0x20
004737A6  mov      ebx, edx
004737A8  test     rcx, rcx
004737AB  je       0x4737c6  ; -> 004737C6
004737AD  call     0x3589b0  ; -> 003589B0 fn
004737B2  mov      r8d, ebx
004737B5  mov      edx, 1
004737BA  mov      ecx, eax
004737BC  add      rsp, 0x20
004737C0  pop      rbx
004737C1  jmp      0x3206e0  ; -> 003206E0 fn
004737C6  xor      eax, eax
004737C8  add      rsp, 0x20
004737CC  pop      rbx
004737CD  ret      
```

## 005A0AF0 (64 B, extent 005A0AF0-005A0B30)

Documented callee on this page: `0080F420`

```
005A0AF0  push     rbx
005A0AF2  sub      rsp, 0x30
005A0AF6  movaps   xmmword ptr [rsp + 0x20], xmm6
005A0AFB  mov      rbx, rdx
005A0AFE  call     qword ptr [rcx + 8]
005A0B01  mov      edx, 1
005A0B06  mov      rcx, rbx
005A0B09  movaps   xmm6, xmm0
005A0B0C  call     0x80f420  ; -> 0080F420 fn
005A0B11  xorps    xmm1, xmm1
005A0B14  mov      rcx, rbx
005A0B17  cvtsd2ss xmm1, xmm6
005A0B1B  call     0x810640  ; -> 00810640 fn
005A0B20  movaps   xmm6, xmmword ptr [rsp + 0x20]
005A0B25  mov      eax, 1
005A0B2A  add      rsp, 0x30
005A0B2E  pop      rbx
005A0B2F  ret      
```

## 005C1350 (60 B, extent 005C1350-005C138C)

Documented callee on this page: `0080F420`

```
005C1350  push     rbx
005C1352  sub      rsp, 0x30
005C1356  movaps   xmmword ptr [rsp + 0x20], xmm6
005C135B  mov      rbx, rdx
005C135E  call     qword ptr [rcx + 8]
005C1361  mov      edx, 1
005C1366  mov      rcx, rbx
005C1369  movaps   xmm6, xmm0
005C136C  call     0x80f420  ; -> 0080F420 fn
005C1371  movaps   xmm1, xmm6
005C1374  mov      rcx, rbx
005C1377  call     0x810640  ; -> 00810640 fn
005C137C  movaps   xmm6, xmmword ptr [rsp + 0x20]
005C1381  mov      eax, 1
005C1386  add      rsp, 0x30
005C138A  pop      rbx
005C138B  ret      
```
