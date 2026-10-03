# F homing pack (FABLE): `25-EBP-Script-Container/Container/ebp2-container.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003545B0 (184 B, extent 003545B0-00354668)

Documented callee on this page: `002673A0`

```
003545B0  mov      qword ptr [rsp + 8], rbx
003545B5  mov      qword ptr [rsp + 0x10], rbp
003545BA  mov      qword ptr [rsp + 0x18], rsi
003545BF  mov      qword ptr [rsp + 0x20], rdi
003545C4  push     r12
003545C6  push     r14
003545C8  push     r15
003545CA  sub      rsp, 0x30
003545CE  mov      rbx, r9
003545D1  call     0x2640c0  ; -> 002640C0 fn
003545D6  mov      rcx, rbx
003545D9  mov      rdi, rax
003545DC  call     0x267e10  ; -> 00267E10 fn
003545E1  mov      rcx, rbx
003545E4  mov      esi, eax
003545E6  call     0x267e10  ; -> 00267E10 fn
003545EB  mov      rcx, rbx
003545EE  mov      ebp, eax
003545F0  call     0x267e10  ; -> 00267E10 fn
003545F5  mov      rcx, rbx
003545F8  mov      r14d, eax
003545FB  call     0x267e10  ; -> 00267E10 fn
00354600  mov      rcx, rbx
00354603  mov      r15d, eax
00354606  call     0x267e10  ; -> 00267E10 fn
0035460B  mov      edx, eax
0035460D  mov      rcx, rdi
00354610  mov      ebx, eax
00354612  call     0x264d60  ; -> 00264D60 fn
00354617  mov      edx, ebx
00354619  mov      rcx, rdi
0035461C  mov      r12, rax
0035461F  call     0x2673a0  ; -> 002673A0 fn
00354624  test     eax, eax
00354626  jne      0x354649  ; -> 00354649
00354628  mov      rcx, qword ptr [rdi + 0xb0]
0035462F  mov      r9d, ebp
00354632  mov      qword ptr [rsp + 0x28], rcx
00354637  mov      r8d, r14d
0035463A  mov      rcx, r12
0035463D  mov      dword ptr [rsp + 0x20], esi
00354641  mov      edx, r15d
00354644  call     0x474070  ; -> 00474070 fn
00354649  mov      rbx, qword ptr [rsp + 0x50]
0035464E  mov      rbp, qword ptr [rsp + 0x58]
00354653  mov      rsi, qword ptr [rsp + 0x60]
00354658  mov      rdi, qword ptr [rsp + 0x68]
0035465D  add      rsp, 0x30
00354661  pop      r15
00354663  pop      r14
00354665  pop      r12
00354667  ret      
```
