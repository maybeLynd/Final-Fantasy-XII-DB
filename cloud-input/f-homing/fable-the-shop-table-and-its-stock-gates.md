# F homing pack (FABLE): `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0027F030 (282 B, extent 0027F030-0027F14A)

Documented callee on this page: `002CCA10`

```
0027F030  push     rdi
0027F032  sub      rsp, 0x30
0027F036  mov      qword ptr [rsp + 0x40], rbx
0027F03B  xor      edi, edi
0027F03D  mov      qword ptr [rsp + 0x48], rbp
0027F042  mov      ebp, r9d
0027F045  mov      qword ptr [rsp + 0x28], r12
0027F04A  mov      ebx, r8d
0027F04D  mov      qword ptr [rsp + 0x20], r15
0027F052  mov      r15d, edx
0027F055  mov      r12d, ecx
0027F058  test     r9d, r9d
0027F05B  jne      0x27f09d  ; -> 0027F09D
0027F05D  cmp      dword ptr [rsp + 0x60], 1
0027F062  je       0x27f112  ; -> 0027F112
0027F068  mov      ecx, ebx
0027F06A  call     0x2cca10  ; -> 002CCA10 fn
0027F06F  test     eax, eax
0027F071  je       0x27f112  ; -> 0027F112
0027F077  mov      rbx, qword ptr [rip + 0x1e1bbb2]  ; -> 0209AC30
0027F07E  mov      ecx, r15d
0027F081  call     0x2ca430  ; -> 002CA430 fn
0027F086  movzx    edx, word ptr [rbx + 0xd68]
0027F08D  mov      ecx, eax
0027F08F  call     0x2cca40  ; -> 002CCA40 fn
0027F094  test     eax, eax
0027F096  jne      0x27f112  ; -> 0027F112
0027F098  lea      edi, [rbp + 4]
0027F09B  jmp      0x27f112  ; -> 0027F112
0027F09D  cmp      ebp, 1
0027F0A0  jne      0x27f112  ; -> 0027F112
0027F0A2  mov      rax, qword ptr [rip + 0x1e1bb87]  ; -> 0209AC30
0027F0A9  mov      ecx, ebx
0027F0AB  mov      qword ptr [rsp + 0x50], rsi
0027F0B0  movzx    esi, byte ptr [rax + 0xd6b]
0027F0B7  call     0x2cca00  ; -> 002CCA00 fn
0027F0BC  test     eax, eax
0027F0BE  je       0x27f10d  ; -> 0027F10D
0027F0C0  mov      ecx, esi
0027F0C2  call     0x2cca00  ; -> 002CCA00 fn
0027F0C7  test     eax, eax
0027F0C9  je       0x27f0d9  ; -> 0027F0D9
0027F0CB  cmp      ebx, esi
0027F0CD  mov      eax, 4
0027F0D2  cmove    eax, edi
0027F0D5  mov      edi, eax
0027F0D7  jmp      0x27f10d  ; -> 0027F10D
0027F0D9  mov      ecx, esi
0027F0DB  call     0x2cca30  ; -> 002CCA30 fn
0027F0E0  test     eax, eax
0027F0E2  jne      0x27f108  ; -> 0027F108
0027F0E4  mov      rax, qword ptr [rip + 0x1e1bb45]  ; -> 0209AC30
0027F0EB  movzx    ecx, word ptr [rax + 0xd48]
0027F0F2  call     0x2ca430  ; -> 002CA430 fn
0027F0F7  mov      ecx, eax
0027F0F9  mov      esi, eax
0027F0FB  call     0x2cca00  ; -> 002CCA00 fn
0027F100  test     eax, eax
0027F102  je       0x27f108  ; -> 0027F108
0027F104  cmp      ebx, esi
0027F106  je       0x27f10d  ; -> 0027F10D
0027F108  mov      edi, 4
0027F10D  mov      rsi, qword ptr [rsp + 0x50]
0027F112  mov      r9d, dword ptr [rsp + 0x60]
0027F117  mov      r8d, ebp
0027F11A  movzx    edx, r15w
0027F11E  movzx    ecx, r12b
0027F122  call     0x317b70  ; -> 00317B70 fn
0027F127  mov      r15, qword ptr [rsp + 0x20]
0027F12C  mov      r12, qword ptr [rsp + 0x28]
0027F131  mov      rbp, qword ptr [rsp + 0x48]
0027F136  mov      rbx, qword ptr [rsp + 0x40]
0027F13B  test     eax, eax
0027F13D  jne      0x27f142  ; -> 0027F142
0027F13F  or       edi, 1
0027F142  mov      eax, edi
0027F144  add      rsp, 0x30
0027F148  pop      rdi
0027F149  ret      
```
