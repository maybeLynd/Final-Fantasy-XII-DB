# F homing pack (FABLE): `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 0019D420 (240 B, extent 0019D420-0019D510)

Documented callee on this page: `0019D8D0`

```
0019D420  test     edx, edx
0019D422  je       0x19d50f  ; -> 0019D50F
0019D428  push     rdi
0019D429  sub      rsp, 0x40
0019D42D  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019D436  mov      qword ptr [rsp + 0x50], rbx
0019D43B  mov      qword ptr [rsp + 0x58], rsi
0019D440  mov      rsi, r8
0019D443  mov      edi, edx
0019D445  mov      rbx, rcx
0019D448  nop      dword ptr [rax + rax]
0019D450  mov      qword ptr [rsp + 0x28], rbx
0019D455  mov      qword ptr [rsp + 0x30], rbx
0019D45A  test     rbx, rbx
0019D45D  je       0x19d4f0  ; -> 0019D4F0
0019D463  mov      rcx, rbx
0019D466  mov      rax, rsi
0019D469  mov      edx, 2
0019D46E  nop      
0019D470  movups   xmm0, xmmword ptr [rax]
0019D473  movups   xmmword ptr [rcx], xmm0
0019D476  movups   xmm1, xmmword ptr [rax + 0x10]
0019D47A  movups   xmmword ptr [rcx + 0x10], xmm1
0019D47E  movups   xmm0, xmmword ptr [rax + 0x20]
0019D482  movups   xmmword ptr [rcx + 0x20], xmm0
0019D486  movups   xmm1, xmmword ptr [rax + 0x30]
0019D48A  movups   xmmword ptr [rcx + 0x30], xmm1
0019D48E  movups   xmm0, xmmword ptr [rax + 0x40]
0019D492  movups   xmmword ptr [rcx + 0x40], xmm0
0019D496  movups   xmm1, xmmword ptr [rax + 0x50]
0019D49A  movups   xmmword ptr [rcx + 0x50], xmm1
0019D49E  movups   xmm0, xmmword ptr [rax + 0x60]
0019D4A2  movups   xmmword ptr [rcx + 0x60], xmm0
0019D4A6  lea      rcx, [rcx + 0x80]
0019D4AD  movups   xmm1, xmmword ptr [rax + 0x70]
0019D4B1  movups   xmmword ptr [rcx - 0x10], xmm1
0019D4B5  lea      rax, [rax + 0x80]
0019D4BC  sub      rdx, 1
0019D4C0  jne      0x19d470  ; -> 0019D470
0019D4C2  lea      rdx, [rsi + 0x100]
0019D4C9  lea      rcx, [rbx + 0x100]
0019D4D0  call     0x19d8d0  ; -> 0019D8D0 fn
0019D4D5  mov      rax, qword ptr [rsi + 0x120]
0019D4DC  mov      qword ptr [rbx + 0x120], rax
0019D4E3  movzx    eax, byte ptr [rsi + 0x128]
0019D4EA  mov      byte ptr [rbx + 0x128], al
0019D4F0  add      rbx, 0x130
0019D4F7  add      edi, -1
0019D4FA  jne      0x19d450  ; -> 0019D450
0019D500  mov      rbx, qword ptr [rsp + 0x50]
0019D505  mov      rsi, qword ptr [rsp + 0x58]
0019D50A  add      rsp, 0x40
0019D50E  pop      rdi
0019D50F  ret      
```

## 0019D970 (183 B, extent 0019D970-0019DA27)

Documented callee on this page: `0019D8D0`

```
0019D970  mov      qword ptr [rsp + 8], rbx
0019D975  push     rdi
0019D976  sub      rsp, 0x20
0019D97A  mov      rbx, rcx
0019D97D  mov      r8, rcx
0019D980  mov      ecx, 2
0019D985  mov      rdi, rdx
0019D988  mov      rax, rdx
0019D98B  nop      dword ptr [rax + rax]
0019D990  lea      r8, [r8 + 0x80]
0019D997  movups   xmm0, xmmword ptr [rax]
0019D99A  lea      rax, [rax + 0x80]
0019D9A1  movups   xmmword ptr [r8 - 0x80], xmm0
0019D9A6  movups   xmm1, xmmword ptr [rax - 0x70]
0019D9AA  movups   xmmword ptr [r8 - 0x70], xmm1
0019D9AF  movups   xmm0, xmmword ptr [rax - 0x60]
0019D9B3  movups   xmmword ptr [r8 - 0x60], xmm0
0019D9B8  movups   xmm1, xmmword ptr [rax - 0x50]
0019D9BC  movups   xmmword ptr [r8 - 0x50], xmm1
0019D9C1  movups   xmm0, xmmword ptr [rax - 0x40]
0019D9C5  movups   xmmword ptr [r8 - 0x40], xmm0
0019D9CA  movups   xmm1, xmmword ptr [rax - 0x30]
0019D9CE  movups   xmmword ptr [r8 - 0x30], xmm1
0019D9D3  movups   xmm0, xmmword ptr [rax - 0x20]
0019D9D7  movups   xmmword ptr [r8 - 0x20], xmm0
0019D9DC  movups   xmm1, xmmword ptr [rax - 0x10]
0019D9E0  movups   xmmword ptr [r8 - 0x10], xmm1
0019D9E5  sub      rcx, 1
0019D9E9  jne      0x19d990  ; -> 0019D990
0019D9EB  add      rdx, 0x100
0019D9F2  lea      rcx, [rbx + 0x100]
0019D9F9  call     0x19d8d0  ; -> 0019D8D0 fn
0019D9FE  mov      rax, qword ptr [rdi + 0x120]
0019DA05  mov      qword ptr [rbx + 0x120], rax
0019DA0C  movzx    eax, byte ptr [rdi + 0x128]
0019DA13  mov      byte ptr [rbx + 0x128], al
0019DA19  mov      rax, rbx
0019DA1C  mov      rbx, qword ptr [rsp + 0x30]
0019DA21  add      rsp, 0x20
0019DA25  pop      rdi
0019DA26  ret      
```

## 001AAE70 (102 B, extent 001AAE70-001AAED6)

Documented callee on this page: `001AB350`

```
001AAE70  push     rbx
001AAE72  sub      rsp, 0x30
001AAE76  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AAE7F  mov      rbx, rcx
001AAE82  mov      r8, qword ptr [rcx + 8]
001AAE86  mov      rdx, qword ptr [rcx]
001AAE89  call     0x1ab350  ; -> 001AB350 fn
001AAE8E  nop      
001AAE8F  mov      r10, qword ptr [rbx]
001AAE92  test     r10, r10
001AAE95  je       0x1aaed0  ; -> 001AAED0
001AAE97  lea      rcx, [rbx + 0x18]
001AAE9B  mov      r9, qword ptr [rcx]
001AAE9E  mov      r8, qword ptr [rbx + 0x10]
001AAEA2  sub      r8, r10
001AAEA5  movabs   rax, 0x2aaaaaaaaaaaaaab
001AAEAF  imul     r8
001AAEB2  sar      rdx, 3
001AAEB6  mov      rax, rdx
001AAEB9  shr      rax, 0x3f
001AAEBD  add      rdx, rax
001AAEC0  lea      r8, [rdx + rdx*2]
001AAEC4  shl      r8, 4
001AAEC8  mov      rdx, r10
001AAECB  call     qword ptr [r9 + 0x18]
001AAECF  nop      
001AAED0  add      rsp, 0x30
001AAED4  pop      rbx
001AAED5  ret      
```

## 001AD0C0 (112 B, extent 001AD0C0-001AD130)

Documented callee on this page: `001AB8A0`

```
001AD0C0  push     rdi
001AD0C2  sub      rsp, 0x30
001AD0C6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AD0CF  mov      qword ptr [rsp + 0x48], rbx
001AD0D4  mov      rdi, rdx
001AD0D7  mov      rbx, qword ptr [rcx + 8]
001AD0DB  cmp      rbx, qword ptr [rcx + 0x10]
001AD0DF  jae      0x1ad11a  ; -> 001AD11A
001AD0E1  mov      qword ptr [rsp + 0x40], rbx
001AD0E6  lea      rax, [rbx + 0x30]
001AD0EA  mov      qword ptr [rcx + 8], rax
001AD0EE  mov      qword ptr [rsp + 0x50], rbx
001AD0F3  test     rbx, rbx
001AD0F6  je       0x1ad118  ; -> 001AD118
001AD0F8  mov      eax, dword ptr [rdx]
001AD0FA  mov      dword ptr [rbx], eax
001AD0FC  movzx    eax, word ptr [rdx + 4]
001AD100  mov      word ptr [rbx + 4], ax
001AD104  add      rdx, 8
001AD108  lea      rcx, [rbx + 8]
001AD10C  call     0x19d8d0  ; -> 0019D8D0 fn
001AD111  movzx    eax, byte ptr [rdi + 0x28]
001AD115  mov      byte ptr [rbx + 0x28], al
001AD118  jmp      0x1ad125  ; -> 001AD125
001AD11A  mov      r8, rdi
001AD11D  mov      rdx, rbx
001AD120  call     0x1ab8a0  ; -> 001AB8A0 fn
001AD125  mov      rbx, qword ptr [rsp + 0x48]
001AD12A  add      rsp, 0x30
001AD12E  pop      rdi
001AD12F  ret      
```

## 001B6A70 (213 B, extent 001B6A70-001B6B45)

Documented callee on this page: `00185A90`

```
001B6A70  mov      qword ptr [rsp + 0x10], rbx
001B6A75  mov      qword ptr [rsp + 0x18], rbp
001B6A7A  mov      qword ptr [rsp + 0x20], rsi
001B6A7F  push     rdi
001B6A80  sub      rsp, 0x20
001B6A84  mov      rbx, qword ptr [rcx + 0x80]
001B6A8B  lea      rdi, [rcx + 0x78]
001B6A8F  mov      rbp, rcx
001B6A92  cmp      rbx, rdi
001B6A95  je       0x1b6abf  ; -> 001B6ABF
001B6A97  call     0x189120  ; -> 00189120 fn
001B6A9C  mov      r8, qword ptr [rbx + 0x20]
001B6AA0  lea      rdx, [rip + 0x189]  ; -> 001B6C30
001B6AA7  mov      rcx, rax
001B6AAA  call     0x185a90  ; -> 00185A90 fn
001B6AAF  mov      rcx, rbx
001B6AB2  call     0x16d6d0  ; -> 0016D6D0 fn
001B6AB7  mov      rbx, rax
001B6ABA  cmp      rax, rdi
001B6ABD  jne      0x1b6a97  ; -> 001B6A97
001B6ABF  mov      rsi, qword ptr [rbp + 0x88]
001B6AC6  test     rsi, rsi
001B6AC9  je       0x1b6b07  ; -> 001B6B07
001B6ACB  mov      qword ptr [rsp + 0x30], r14
001B6AD0  mov      rdx, qword ptr [rsi]
001B6AD3  lea      rcx, [rbp + 0x70]
001B6AD7  call     0x220390  ; -> 00220390 fn
001B6ADC  mov      rax, qword ptr [rbp + 0xa0]
001B6AE3  lea      rcx, [rbp + 0xa0]
001B6AEA  mov      rbx, qword ptr [rsi + 8]
001B6AEE  mov      r8d, 0x28
001B6AF4  mov      rdx, rsi
001B6AF7  call     qword ptr [rax + 0x18]
001B6AFA  mov      rsi, rbx
001B6AFD  test     rbx, rbx
001B6B00  jne      0x1b6ad0  ; -> 001B6AD0
001B6B02  mov      r14, qword ptr [rsp + 0x30]
001B6B07  mov      rbx, qword ptr [rsp + 0x38]
001B6B0C  lea      rax, [rbp + 0x78]
001B6B10  mov      rsi, qword ptr [rsp + 0x48]
001B6B15  mov      qword ptr [rbp + 0x80], rax
001B6B1C  mov      qword ptr [rax], rax
001B6B1F  xor      eax, eax
001B6B21  mov      qword ptr [rbp + 0x88], rax
001B6B28  mov      byte ptr [rbp + 0x90], al
001B6B2E  mov      dword ptr [rbp + 0x98], eax
001B6B34  cmp      dword ptr [rbp + 0x60], eax
001B6B37  mov      rbp, qword ptr [rsp + 0x40]
001B6B3C  sete     al
001B6B3F  add      rsp, 0x20
001B6B43  pop      rdi
001B6B44  ret      
```
