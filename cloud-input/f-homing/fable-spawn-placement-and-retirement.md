# F homing pack (FABLE): `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 6. No bearing page cites them and no documented function calls them directly.

## 00290300 (17 B, extent 00290300-00290311)

Documented callee on this page: `00291010`

```
00290300  mov      r8d, edx
00290303  mov      edx, ecx
00290305  mov      rcx, qword ptr [rip + 0x1e0bb74]  ; -> 0209BE80
0029030C  jmp      0x291010  ; -> 00291010 fn
```

## 00311E90 (177 B, extent 00311E90-00311F41)

Documented callee on this page: `0031B810`

```
00311E90  mov      qword ptr [rsp + 8], rbx
00311E95  mov      qword ptr [rsp + 0x10], rbp
00311E9A  mov      qword ptr [rsp + 0x18], rsi
00311E9F  push     rdi
00311EA0  push     r14
00311EA2  push     r15
00311EA4  sub      rsp, 0x20
00311EA8  xor      ebx, ebx
00311EAA  lea      r15, [rip + 0x1faf8d7]  ; -> 022C1788
00311EB1  mov      r14d, ebx
00311EB4  mov      esi, ebx
00311EB6  mov      edi, ebx
00311EB8  mov      ecx, esi
00311EBA  call     0x31b810  ; -> 0031B810 fn
00311EBF  mov      rbp, rax
00311EC2  test     rax, rax
00311EC5  je       0x311efa  ; -> 00311EFA
00311EC7  mov      rax, qword ptr [rax + 0x698]
00311ECE  test     rax, rax
00311ED1  je       0x311efa  ; -> 00311EFA
00311ED3  mov      ecx, dword ptr [rax + 0x64]
00311ED6  or       ecx, dword ptr [rax + 0x3c]
00311ED9  test     ecx, 0x80000003
00311EDF  je       0x311eea  ; -> 00311EEA
00311EE1  call     0x377c20  ; -> 00377C20 fn
00311EE6  test     eax, eax
00311EE8  je       0x311efa  ; -> 00311EFA
00311EEA  cmp      rdi, 4
00311EEE  jge      0x311ef4  ; -> 00311EF4
00311EF0  mov      qword ptr [r15 + rdi*8], rbp
00311EF4  inc      r14d
00311EF7  inc      rdi
00311EFA  inc      esi
00311EFC  cmp      esi, 4
00311EFF  jl       0x311eb8  ; -> 00311EB8
00311F01  movsxd   rcx, r14d
00311F04  test     r14d, r14d
00311F07  jle      0x311f28  ; -> 00311F28
00311F09  nop      dword ptr [rax]
00311F10  mov      rax, qword ptr [r15 + rbx*8]
00311F14  test     rax, rax
00311F17  je       0x311f20  ; -> 00311F20
00311F19  or       dword ptr [rax + 4], 0x600
00311F20  inc      rbx
00311F23  cmp      rbx, rcx
00311F26  jl       0x311f10  ; -> 00311F10
00311F28  mov      rbx, qword ptr [rsp + 0x40]
00311F2D  mov      rbp, qword ptr [rsp + 0x48]
00311F32  mov      rsi, qword ptr [rsp + 0x50]
00311F37  add      rsp, 0x20
00311F3B  pop      r15
00311F3D  pop      r14
00311F3F  pop      rdi
00311F40  ret      
```

## 0032A830 (24 B, extent 0032A830-0032A848)

Documented callee on this page: `00300BA0`

```
0032A830  sub      rsp, 0x28
0032A834  xor      r8d, r8d
0032A837  call     0x300ba0  ; -> 00300BA0 fn
0032A83C  xor      ecx, ecx
0032A83E  test     eax, eax
0032A840  cmovs    eax, ecx
0032A843  add      rsp, 0x28
0032A847  ret      
```

## 00330050 (8 B, extent 00330050-00330058)

Documented callee on this page: `0032ED80`

```
00330050  mov      ecx, dword ptr [rcx + 0x28]
00330053  jmp      0x32ed80  ; -> 0032ED80 fn
```

## 00350100 (92 B, extent 00350100-0035015C)

Documented callee on this page: `003EBD00`

```
00350100  mov      qword ptr [rsp + 8], rbx
00350105  push     rdi
00350106  sub      rsp, 0x20
0035010A  mov      rcx, r9
0035010D  mov      rbx, r9
00350110  call     0x267e10  ; -> 00267E10 fn
00350115  mov      rcx, rbx
00350118  mov      edi, eax
0035011A  call     0x267e10  ; -> 00267E10 fn
0035011F  add      eax, 3
00350122  cmp      eax, 3
00350125  jge      0x35012e  ; -> 0035012E
00350127  mov      eax, 3
0035012C  jmp      0x350138  ; -> 00350138
0035012E  mov      ecx, 4
00350133  cmp      eax, ecx
00350135  cmovg    eax, ecx
00350138  mov      ecx, eax
0035013A  test     edi, edi
0035013C  je       0x35014d  ; -> 0035014D
0035013E  mov      rbx, qword ptr [rsp + 0x30]
00350143  add      rsp, 0x20
00350147  pop      rdi
00350148  jmp      0x3ebb90  ; -> 003EBB90 fn
0035014D  mov      rbx, qword ptr [rsp + 0x30]
00350152  add      rsp, 0x20
00350156  pop      rdi
00350157  jmp      0x3ebd00  ; -> 003EBD00 fn
```

## 0050C800 (65 B, extent 0050C800-0050C841)

Documented callee on this page: `0036FCC0`

```
0050C800  push     rdi
0050C802  sub      rsp, 0x20
0050C806  cmp      dword ptr [r8], 0
0050C80A  mov      rdi, r8
0050C80D  jne      0x50c839  ; -> 0050C839
0050C80F  mov      qword ptr [rsp + 0x30], rbx
0050C814  call     0x36fcc0  ; -> 0036FCC0 fn
0050C819  xor      ebx, ebx
0050C81B  nop      dword ptr [rax + rax]
0050C820  mov      ecx, ebx
0050C822  call     0x26b8e0  ; -> 0026B8E0 fn
0050C827  inc      ebx
0050C829  cmp      ebx, 3
0050C82C  jle      0x50c820  ; -> 0050C820
0050C82E  mov      rbx, qword ptr [rsp + 0x30]
0050C833  mov      dword ptr [rdi], 1
0050C839  xor      eax, eax
0050C83B  add      rsp, 0x20
0050C83F  pop      rdi
0050C840  ret      
```
