# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 4. No bearing page cites them and no documented function calls them directly.

## 003B8030 (85 B, extent 003B8030-003B8085)

Documented callee on this page: `0026B620`

```
003B8030  push     rdi
003B8032  sub      rsp, 0x30
003B8036  xor      edi, edi
003B8038  movaps   xmmword ptr [rsp + 0x20], xmm6
003B803D  cmp      dword ptr [rip + 0x2b04b7d], edi  ; -> 02EBCBC0
003B8043  movaps   xmm6, xmm0
003B8046  jle      0x3b807a  ; -> 003B807A
003B8048  mov      qword ptr [rsp + 0x40], rbx
003B804D  lea      rbx, [rip + 0x2b04a6c]  ; -> 02EBCAC0
003B8054  mov      rcx, qword ptr [rbx]
003B8057  call     0x263f40  ; -> 00263F40 fn
003B805C  movaps   xmm1, xmm6
003B805F  mov      rcx, rax
003B8062  call     0x26b620  ; -> 0026B620 fn
003B8067  inc      edi
003B8069  lea      rbx, [rbx + 8]
003B806D  cmp      edi, dword ptr [rip + 0x2b04b4d]  ; -> 02EBCBC0
003B8073  jl       0x3b8054  ; -> 003B8054
003B8075  mov      rbx, qword ptr [rsp + 0x40]
003B807A  movaps   xmm6, xmmword ptr [rsp + 0x20]
003B807F  add      rsp, 0x30
003B8083  pop      rdi
003B8084  ret      
```

## 0050D3B0 (81 B, extent 0050D3B0-0050D401)

Documented callee on this page: `002650B0`

```
0050D3B0  mov      qword ptr [rsp + 8], rbx
0050D3B5  mov      qword ptr [rsp + 0x10], rsi
0050D3BA  push     rdi
0050D3BB  sub      rsp, 0x20
0050D3BF  mov      rdi, r9
0050D3C2  mov      rsi, rdx
0050D3C5  call     0x2640c0  ; -> 002640C0 fn
0050D3CA  mov      rcx, rdi
0050D3CD  mov      rbx, rax
0050D3D0  call     0x267e10  ; -> 00267E10 fn
0050D3D5  mov      r8d, eax
0050D3D8  mov      rdx, rsi
0050D3DB  mov      rcx, rbx
0050D3DE  call     0x2650b0  ; -> 002650B0 fn
0050D3E3  mov      rdx, rax
0050D3E6  lea      rcx, [rip + 0x81560b]  ; -> 00D229F8
0050D3ED  mov      rbx, qword ptr [rsp + 0x30]
0050D3F2  mov      rsi, qword ptr [rsp + 0x38]
0050D3F7  add      rsp, 0x20
0050D3FB  pop      rdi
0050D3FC  jmp      0x17d280  ; -> 0017D280 fn
```

## 0050D420 (81 B, extent 0050D420-0050D471)

Documented callee on this page: `002650B0`

```
0050D420  mov      qword ptr [rsp + 8], rbx
0050D425  mov      qword ptr [rsp + 0x10], rsi
0050D42A  push     rdi
0050D42B  sub      rsp, 0x20
0050D42F  mov      rdi, r9
0050D432  mov      rsi, rdx
0050D435  call     0x2640c0  ; -> 002640C0 fn
0050D43A  mov      rcx, rdi
0050D43D  mov      rbx, rax
0050D440  call     0x267e10  ; -> 00267E10 fn
0050D445  mov      r8d, eax
0050D448  mov      rdx, rsi
0050D44B  mov      rcx, rbx
0050D44E  call     0x2650b0  ; -> 002650B0 fn
0050D453  mov      rdx, rax
0050D456  lea      rcx, [rip + 0x3e6fdb]  ; -> 008F4438
0050D45D  mov      rbx, qword ptr [rsp + 0x30]
0050D462  mov      rsi, qword ptr [rsp + 0x38]
0050D467  add      rsp, 0x20
0050D46B  pop      rdi
0050D46C  jmp      0x17d280  ; -> 0017D280 fn
```

## 0050EA80 (40 B, extent 0050EA80-0050EAA8)

Documented callee on this page: `0036F000`

```
0050EA80  sub      rsp, 0x28
0050EA84  call     0x36f000  ; -> 0036F000 fn
0050EA89  test     eax, eax
0050EA8B  je       0x50ea94  ; -> 0050EA94
0050EA8D  xor      eax, eax
0050EA8F  add      rsp, 0x28
0050EA93  ret      
0050EA94  mov      ecx, 1
0050EA99  call     0x314d40  ; -> 00314D40 fn
0050EA9E  mov      eax, 1
0050EAA3  add      rsp, 0x28
0050EAA7  ret      
```
