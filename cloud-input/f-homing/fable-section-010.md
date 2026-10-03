# F homing pack (FABLE): `25-EBP-Script-Container/Sections/section-010.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 0034E220 (49 B, extent 0034E220-0034E251)

Documented callee on this page: `002E64E0`

```
0034E220  push     rbx
0034E222  sub      rsp, 0x20
0034E226  mov      rcx, r9
0034E229  mov      rbx, rdx
0034E22C  call     0x267e10  ; -> 00267E10 fn
0034E231  mov      rcx, rbx
0034E234  test     eax, eax
0034E236  je       0x34e242  ; -> 0034E242
0034E238  add      rsp, 0x20
0034E23C  pop      rbx
0034E23D  jmp      0x2e64e0  ; -> 002E64E0 fn
0034E242  xor      r8d, r8d
0034E245  xor      edx, edx
0034E247  add      rsp, 0x20
0034E24B  pop      rbx
0034E24C  jmp      0x2ebe50  ; -> 002EBE50 fn
```

## 003B7A30 (117 B, extent 003B7A30-003B7AA5)

Documented callee on this page: `002693D0`

```
003B7A30  push     rbx
003B7A32  sub      rsp, 0x20
003B7A36  mov      rcx, qword ptr [rip + 0x2b0522b]  ; -> 02EBCC68
003B7A3D  test     rcx, rcx
003B7A40  je       0x3b7a54  ; -> 003B7A54
003B7A42  call     0x263f40  ; -> 00263F40 fn
003B7A47  mov      edx, 1
003B7A4C  mov      rcx, rax
003B7A4F  call     0x2693d0  ; -> 002693D0 fn
003B7A54  mov      eax, dword ptr [rip + 0x2b05166]  ; -> 02EBCBC0
003B7A5A  xor      ebx, ebx
003B7A5C  test     eax, eax
003B7A5E  jle      0x3b7a9f  ; -> 003B7A9F
003B7A60  mov      qword ptr [rsp + 0x30], rdi
003B7A65  lea      rdi, [rip + 0x2b05054]  ; -> 02EBCAC0
003B7A6C  nop      dword ptr [rax]
003B7A70  mov      rcx, qword ptr [rdi]
003B7A73  test     rcx, rcx
003B7A76  je       0x3b7a90  ; -> 003B7A90
003B7A78  call     0x263f40  ; -> 00263F40 fn
003B7A7D  mov      edx, 1
003B7A82  mov      rcx, rax
003B7A85  call     0x2693d0  ; -> 002693D0 fn
003B7A8A  mov      eax, dword ptr [rip + 0x2b05130]  ; -> 02EBCBC0
003B7A90  inc      ebx
003B7A92  add      rdi, 8
003B7A96  cmp      ebx, eax
003B7A98  jl       0x3b7a70  ; -> 003B7A70
003B7A9A  mov      rdi, qword ptr [rsp + 0x30]
003B7A9F  add      rsp, 0x20
003B7AA3  pop      rbx
003B7AA4  ret      
```

## 003B7AB0 (78 B, extent 003B7AB0-003B7AFE)

Documented callee on this page: `002693D0`

```
003B7AB0  push     rbx
003B7AB2  sub      rsp, 0x20
003B7AB6  xor      ebx, ebx
003B7AB8  cmp      dword ptr [rip + 0x2b04fe2], ebx  ; -> 02EBCAA0
003B7ABE  jle      0x3b7af8  ; -> 003B7AF8
003B7AC0  mov      qword ptr [rsp + 0x30], rdi
003B7AC5  lea      rdi, [rip + 0x2b04fb4]  ; -> 02EBCA80
003B7ACC  nop      dword ptr [rax]
003B7AD0  mov      rcx, qword ptr [rdi]
003B7AD3  call     0x263f40  ; -> 00263F40 fn
003B7AD8  mov      edx, 1
003B7ADD  mov      rcx, rax
003B7AE0  call     0x2693d0  ; -> 002693D0 fn
003B7AE5  inc      ebx
003B7AE7  lea      rdi, [rdi + 8]
003B7AEB  cmp      ebx, dword ptr [rip + 0x2b04faf]  ; -> 02EBCAA0
003B7AF1  jl       0x3b7ad0  ; -> 003B7AD0
003B7AF3  mov      rdi, qword ptr [rsp + 0x30]
003B7AF8  add      rsp, 0x20
003B7AFC  pop      rbx
003B7AFD  ret      
```
