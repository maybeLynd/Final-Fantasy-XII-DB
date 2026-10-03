# F homing pack (FABLE): `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0019CD40 (155 B, extent 0019CD40-0019CDDB)

Documented callee on this page: `0020BB10`

```
0019CD40  push     rbx
0019CD42  sub      rsp, 0x40
0019CD46  mov      r10, qword ptr [rcx + 8]
0019CD4A  movabs   rax, 0x2aaaaaaaaaaaaaab
0019CD54  mov      r9, qword ptr [rcx]
0019CD57  mov      r8, r10
0019CD5A  mov      r11d, edx
0019CD5D  sub      r8, r9
0019CD60  imul     r8
0019CD63  mov      rbx, rcx
0019CD66  sar      rdx, 2
0019CD6A  mov      rax, rdx
0019CD6D  shr      rax, 0x3f
0019CD71  add      rdx, rax
0019CD74  cmp      r11d, edx
0019CD77  jbe      0x19cda3  ; -> 0019CDA3
0019CD79  xor      eax, eax
0019CD7B  lea      r9, [rsp + 0x20]
0019CD80  sub      r11d, edx
0019CD83  mov      qword ptr [rsp + 0x20], rax
0019CD88  mov      r8d, r11d
0019CD8B  mov      qword ptr [rsp + 0x28], rax
0019CD90  mov      rdx, r10
0019CD93  mov      qword ptr [rsp + 0x30], rax
0019CD98  call     0x20bb10  ; -> 0020BB10 fn
0019CD9D  add      rsp, 0x40
0019CDA1  pop      rbx
0019CDA2  ret      
0019CDA3  lea      rcx, [r11 + r11*2]
0019CDA7  movabs   rax, 0xd555555555555555
0019CDB1  lea      rdx, [r9 + rcx*8]
0019CDB5  sub      r10, rdx
0019CDB8  imul     r10
0019CDBB  sar      rdx, 2
0019CDBF  mov      rax, rdx
0019CDC2  shr      rax, 0x3f
0019CDC6  add      rdx, rax
0019CDC9  lea      rax, [rdx + rdx*2]
0019CDCD  shl      rax, 3
0019CDD1  add      qword ptr [rbx + 8], rax
0019CDD5  add      rsp, 0x40
0019CDD9  pop      rbx
0019CDDA  ret      
```
