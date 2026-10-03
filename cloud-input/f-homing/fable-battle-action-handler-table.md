# F homing pack (FABLE): `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00346780 (185 B, extent 00346780-00346839)

Documented callee on this page: `00265060`

```
00346780  mov      qword ptr [rsp + 8], rbx
00346785  mov      qword ptr [rsp + 0x10], rbp
0034678A  mov      qword ptr [rsp + 0x18], rsi
0034678F  mov      qword ptr [rsp + 0x20], rdi
00346794  push     r14
00346796  sub      rsp, 0x40
0034679A  mov      r14, rcx
0034679D  movaps   xmmword ptr [rsp + 0x30], xmm6
003467A2  mov      rcx, r9
003467A5  mov      rbx, r9
003467A8  mov      rbp, rdx
003467AB  call     0x267e10  ; -> 00267E10 fn
003467B0  mov      rcx, rbx
003467B3  mov      edi, eax
003467B5  call     0x267db0  ; -> 00267DB0 fn
003467BA  movaps   xmm6, xmm0
003467BD  mov      rcx, rbp
003467C0  mulss    xmm6, dword ptr [rip + 0x19a53a8]  ; -> 01CEBB70 [f32 0.5]
003467C8  call     0x265060  ; -> 00265060 fn
003467CD  mov      ecx, edi
003467CF  mov      rsi, rax
003467D2  call     0x264010  ; -> 00264010 fn
003467D7  mov      rcx, rax
003467DA  call     0x265060  ; -> 00265060 fn
003467DF  mov      rcx, rbp
003467E2  mov      rbx, rax
003467E5  call     0x265200  ; -> 00265200 fn
003467EA  movss    xmm2, dword ptr [rbx + 8]
003467EF  movaps   xmm1, xmm6
003467F2  movss    xmm3, dword ptr [rbx]
003467F6  movss    dword ptr [rsp + 0x28], xmm2
003467FC  movss    xmm2, dword ptr [rsi]
00346800  movss    dword ptr [rsp + 0x20], xmm3
00346806  movss    xmm3, dword ptr [rsi + 8]
0034680B  call     0x3a1bb0  ; -> 003A1BB0 fn
00346810  mov      edx, eax
00346812  mov      rcx, r14
00346815  mov      rbx, qword ptr [rsp + 0x50]
0034681A  mov      rbp, qword ptr [rsp + 0x58]
0034681F  mov      rsi, qword ptr [rsp + 0x60]
00346824  mov      rdi, qword ptr [rsp + 0x68]
00346829  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034682E  add      rsp, 0x40
00346832  pop      r14
00346834  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00346EF0 (172 B, extent 00346EF0-00346F9C)

Documented callee on this page: `00265060`

```
00346EF0  mov      qword ptr [rsp + 8], rbx
00346EF5  mov      qword ptr [rsp + 0x10], rsi
00346EFA  push     rdi
00346EFB  sub      rsp, 0x60
00346EFF  movaps   xmmword ptr [rsp + 0x50], xmm6
00346F04  mov      rsi, rcx
00346F07  movaps   xmmword ptr [rsp + 0x40], xmm7
00346F0C  mov      rcx, r9
00346F0F  movaps   xmmword ptr [rsp + 0x30], xmm8
00346F15  mov      rbx, r9
00346F18  mov      rdi, rdx
00346F1B  call     0x267db0  ; -> 00267DB0 fn
00346F20  mov      rcx, rbx
00346F23  movaps   xmm8, xmm0
00346F27  call     0x267db0  ; -> 00267DB0 fn
00346F2C  mov      rcx, rbx
00346F2F  movaps   xmm6, xmm0
00346F32  call     0x267db0  ; -> 00267DB0 fn
00346F37  movaps   xmm7, xmm0
00346F3A  mov      rcx, rdi
00346F3D  mulss    xmm7, dword ptr [rip + 0x19a4c2b]  ; -> 01CEBB70 [f32 0.5]
00346F45  call     0x265060  ; -> 00265060 fn
00346F4A  mov      rcx, rdi
00346F4D  mov      rbx, rax
00346F50  call     0x265200  ; -> 00265200 fn
00346F55  movss    xmm3, dword ptr [rbx + 8]
00346F5A  movaps   xmm1, xmm7
00346F5D  movss    xmm2, dword ptr [rbx]
00346F61  movss    dword ptr [rsp + 0x28], xmm8
00346F68  movss    dword ptr [rsp + 0x20], xmm6
00346F6E  call     0x3a1bb0  ; -> 003A1BB0 fn
00346F73  mov      edx, eax
00346F75  mov      rcx, rsi
00346F78  mov      rbx, qword ptr [rsp + 0x70]
00346F7D  mov      rsi, qword ptr [rsp + 0x78]
00346F82  movaps   xmm6, xmmword ptr [rsp + 0x50]
00346F87  movaps   xmm7, xmmword ptr [rsp + 0x40]
00346F8C  movaps   xmm8, xmmword ptr [rsp + 0x30]
00346F92  add      rsp, 0x60
00346F96  pop      rdi
00346F97  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
