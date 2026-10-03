# F homing pack (FABLE): `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 0035AA50 (194 B, extent 0035AA50-0035AB12)

Documented callee on this page: `00263BE0`

```
0035AA50  mov      qword ptr [rsp + 8], rbx
0035AA55  mov      qword ptr [rsp + 0x10], rbp
0035AA5A  mov      qword ptr [rsp + 0x18], rsi
0035AA5F  push     rdi
0035AA60  push     r14
0035AA62  push     r15
0035AA64  sub      rsp, 0x20
0035AA68  mov      ebp, r8d
0035AA6B  mov      r15d, edx
0035AA6E  call     0x263ff0  ; -> 00263FF0 fn
0035AA73  mov      r14, rax
0035AA76  movzx    ebx, word ptr [rax + 0x1de]
0035AA7D  movzx    esi, word ptr [rax + 0x1d6]
0035AA84  add      esi, ebx
0035AA86  test     r15d, r15d
0035AA89  js       0x35aac8  ; -> 0035AAC8
0035AA8B  cmp      ebx, esi
0035AA8D  jae      0x35aaf9  ; -> 0035AAF9
0035AA8F  nop      
0035AA90  mov      edx, ebx
0035AA92  mov      rcx, r14
0035AA95  call     0x358940  ; -> 00358940 fn
0035AA9A  mov      rcx, rax
0035AA9D  mov      rdi, rax
0035AAA0  call     0x263be0  ; -> 00263BE0 fn
0035AAA5  cmp      eax, r15d
0035AAA8  jne      0x35aac0  ; -> 0035AAC0
0035AAAA  mov      rcx, rdi
0035AAAD  call     0x2647b0  ; -> 002647B0 fn
0035AAB2  test     eax, eax
0035AAB4  jne      0x35aac0  ; -> 0035AAC0
0035AAB6  mov      edx, ebp
0035AAB8  mov      rcx, rdi
0035AABB  call     0x26dc40  ; -> 0026DC40 fn
0035AAC0  inc      ebx
0035AAC2  cmp      ebx, esi
0035AAC4  jl       0x35aa90  ; -> 0035AA90
0035AAC6  jmp      0x35aaf9  ; -> 0035AAF9
0035AAC8  cmp      ebx, esi
0035AACA  jae      0x35aaf9  ; -> 0035AAF9
0035AACC  nop      dword ptr [rax]
0035AAD0  mov      edx, ebx
0035AAD2  mov      rcx, r14
0035AAD5  call     0x358940  ; -> 00358940 fn
0035AADA  mov      rcx, rax
0035AADD  mov      rdi, rax
0035AAE0  call     0x2647b0  ; -> 002647B0 fn
0035AAE5  test     eax, eax
0035AAE7  jne      0x35aaf3  ; -> 0035AAF3
0035AAE9  mov      edx, ebp
0035AAEB  mov      rcx, rdi
0035AAEE  call     0x26dc40  ; -> 0026DC40 fn
0035AAF3  inc      ebx
0035AAF5  cmp      ebx, esi
0035AAF7  jl       0x35aad0  ; -> 0035AAD0
0035AAF9  mov      rbx, qword ptr [rsp + 0x40]
0035AAFE  mov      rbp, qword ptr [rsp + 0x48]
0035AB03  mov      rsi, qword ptr [rsp + 0x50]
0035AB08  add      rsp, 0x20
0035AB0C  pop      r15
0035AB0E  pop      r14
0035AB10  pop      rdi
0035AB11  ret      
```

## 003B76B0 (104 B, extent 003B76B0-003B7718)

Documented callee on this page: `002E7600`

```
003B76B0  mov      qword ptr [rsp + 0x18], rbx
003B76B5  push     rbp
003B76B6  sub      rsp, 0x20
003B76BA  xor      ebx, ebx
003B76BC  mov      ebp, ecx
003B76BE  cmp      dword ptr [rip + 0x2b054fc], ebx  ; -> 02EBCBC0
003B76C4  jle      0x3b770d  ; -> 003B770D
003B76C6  mov      qword ptr [rsp + 0x30], rsi
003B76CB  mov      qword ptr [rsp + 0x38], rdi
003B76D0  lea      rdi, [rip + 0x2b053e9]  ; -> 02EBCAC0
003B76D7  mov      rsi, qword ptr [rdi]
003B76DA  test     rsi, rsi
003B76DD  je       0x3b76f5  ; -> 003B76F5
003B76DF  mov      rcx, rsi
003B76E2  call     0x2e7600  ; -> 002E7600 fn
003B76E7  test     eax, eax
003B76E9  je       0x3b76f5  ; -> 003B76F5
003B76EB  mov      edx, ebp
003B76ED  mov      rcx, rsi
003B76F0  call     0x2e7a10  ; -> 002E7A10 fn
003B76F5  inc      ebx
003B76F7  add      rdi, 8
003B76FB  cmp      ebx, dword ptr [rip + 0x2b054bf]  ; -> 02EBCBC0
003B7701  jl       0x3b76d7  ; -> 003B76D7
003B7703  mov      rdi, qword ptr [rsp + 0x38]
003B7708  mov      rsi, qword ptr [rsp + 0x30]
003B770D  mov      rbx, qword ptr [rsp + 0x40]
003B7712  add      rsp, 0x20
003B7716  pop      rbp
003B7717  ret      
```

## 003E9190 (53 B, extent 003E9190-003E91C5)

Documented callee on this page: `002E9FE0`

```
003E9190  push     rbx
003E9192  sub      rsp, 0x20
003E9196  call     0x3590d0  ; -> 003590D0 fn
003E919B  mov      ecx, eax
003E919D  call     0x3588b0  ; -> 003588B0 fn
003E91A2  xor      ebx, ebx
003E91A4  mov      ecx, ebx
003E91A6  call     0x263750  ; -> 00263750 fn
003E91AB  test     rax, rax
003E91AE  je       0x3e91b8  ; -> 003E91B8
003E91B0  mov      rcx, rax
003E91B3  call     0x2e9fe0  ; -> 002E9FE0 fn
003E91B8  inc      ebx
003E91BA  cmp      ebx, 4
003E91BD  jl       0x3e91a4  ; -> 003E91A4
003E91BF  add      rsp, 0x20
003E91C3  pop      rbx
003E91C4  ret      
```
