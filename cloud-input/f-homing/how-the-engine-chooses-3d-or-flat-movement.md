# F homing pack: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

Generated 2026-10-02 22:03 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 003B79D0 (94 B, extent 003B79D0-003B7A2E)

Documented callee on this page: `0017F5B0`

```
003B79D0  push     rbx
003B79D2  sub      rsp, 0x20
003B79D6  cmp      dword ptr [rip + 0x1f06f93], 0  ; -> 022BE970
003B79DD  je       0x3b79e9  ; -> 003B79E9
003B79DF  mov      ecx, 1
003B79E4  call     0x17f5b0  ; -> 0017F5B0 fn
003B79E9  mov      eax, dword ptr [rip + 0x2b051d1]  ; -> 02EBCBC0
003B79EF  xor      ebx, ebx
003B79F1  test     eax, eax
003B79F3  jle      0x3b7a28  ; -> 003B7A28
003B79F5  mov      qword ptr [rsp + 0x30], rdi
003B79FA  lea      rdi, [rip + 0x2b050bf]  ; -> 02EBCAC0
003B7A01  mov      rcx, qword ptr [rdi]
003B7A04  test     rcx, rcx
003B7A07  je       0x3b7a19  ; -> 003B7A19
003B7A09  mov      edx, 0x1049
003B7A0E  call     0x2eb030  ; -> 002EB030 fn
003B7A13  mov      eax, dword ptr [rip + 0x2b051a7]  ; -> 02EBCBC0
003B7A19  inc      ebx
003B7A1B  add      rdi, 8
003B7A1F  cmp      ebx, eax
003B7A21  jl       0x3b7a01  ; -> 003B7A01
003B7A23  mov      rdi, qword ptr [rsp + 0x30]
003B7A28  add      rsp, 0x20
003B7A2C  pop      rbx
003B7A2D  ret      
```

## 003B7D80 (128 B, extent 003B7D80-003B7E00)

Documented callee on this page: `0026B720`

```
003B7D80  push     rbx
003B7D82  sub      rsp, 0x20
003B7D86  xor      ebx, ebx
003B7D88  cmp      dword ptr [rip + 0x2b04ed2], ebx  ; -> 02EBCC60
003B7D8E  jle      0x3b7dfa  ; -> 003B7DFA
003B7D90  mov      qword ptr [rsp + 0x38], rsi
003B7D95  mov      qword ptr [rsp + 0x40], rdi
003B7D9A  lea      rdi, [rip + 0x2b04d1f]  ; -> 02EBCAC0
003B7DA1  mov      qword ptr [rsp + 0x30], rbp
003B7DA6  mov      rsi, qword ptr [rdi]
003B7DA9  test     rsi, rsi
003B7DAC  je       0x3b7ddd  ; -> 003B7DDD
003B7DAE  mov      rcx, rsi
003B7DB1  call     0x263f40  ; -> 00263F40 fn
003B7DB6  mov      rcx, rsi
003B7DB9  mov      rbp, rax
003B7DBC  call     0x359b80  ; -> 00359B80 fn
003B7DC1  test     rax, rax
003B7DC4  je       0x3b7ddd  ; -> 003B7DDD
003B7DC6  movss    xmm3, dword ptr [rax + 0x18]
003B7DCB  mov      rcx, rbp
003B7DCE  movss    xmm2, dword ptr [rax + 0x14]
003B7DD3  movss    xmm1, dword ptr [rax + 0x10]
003B7DD8  call     0x26b720  ; -> 0026B720 fn
003B7DDD  inc      ebx
003B7DDF  add      rdi, 8
003B7DE3  cmp      ebx, dword ptr [rip + 0x2b04e77]  ; -> 02EBCC60
003B7DE9  jl       0x3b7da6  ; -> 003B7DA6
003B7DEB  mov      rdi, qword ptr [rsp + 0x40]
003B7DF0  mov      rsi, qword ptr [rsp + 0x38]
003B7DF5  mov      rbp, qword ptr [rsp + 0x30]
003B7DFA  add      rsp, 0x20
003B7DFE  pop      rbx
003B7DFF  ret      
```
