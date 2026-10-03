# F homing pack (FABLE): `26-PKFL-Package-Container/Container/pkfl-package-container.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003DF2C0 (154 B, extent 003DF2C0-003DF35A)

Documented callee on this page: `0032F3A0`

```
003DF2C0  push     rbx
003DF2C2  sub      rsp, 0x30
003DF2C6  movsxd   rbx, ecx
003DF2C9  lea      rdx, [rsp + 0x20]
003DF2CE  mov      r8d, 2
003DF2D4  mov      rcx, qword ptr [rbx + 0x18]
003DF2D8  call     0x36b970  ; -> 0036B970 fn
003DF2DD  test     eax, eax
003DF2DF  je       0x3df354  ; -> 003DF354
003DF2E1  mov      rax, qword ptr [rsp + 0x20]
003DF2E6  mov      qword ptr [rbx + 0x18], rax
003DF2EA  mov      rax, qword ptr [rsp + 0x28]
003DF2EF  mov      qword ptr [rbx + 0x20], rax
003DF2F3  test     rbx, rbx
003DF2F6  je       0x3df354  ; -> 003DF354
003DF2F8  mov      rax, qword ptr [rbx + 0x18]
003DF2FC  test     rax, rax
003DF2FF  je       0x3df333  ; -> 003DF333
003DF301  cmp      word ptr [rax + 0x10], 0
003DF306  movsx    r8d, word ptr [rax + 0x12]
003DF30B  je       0x3df333  ; -> 003DF333
003DF30D  movsx    ecx, byte ptr [rbx + 0x11]
003DF311  mov      eax, 0x66666667
003DF316  imul     r8d
003DF319  sar      edx, 2
003DF31C  mov      eax, edx
003DF31E  shr      eax, 0x1f
003DF321  add      edx, eax
003DF323  lea      eax, [rdx + rdx*4]
003DF326  add      eax, eax
003DF328  sub      r8d, eax
003DF32B  mov      edx, r8d
003DF32E  call     0x32f3a0  ; -> 0032F3A0 fn
003DF333  movsx    edx, byte ptr [rbx + 0x12]
003DF337  movsx    ecx, byte ptr [rbx + 0x11]
003DF33B  mov      r9, qword ptr [rbx + 0x20]
003DF33F  mov      r8, qword ptr [rbx + 0x18]
003DF343  call     0x3df360  ; -> 003DF360 fn
003DF348  mov      qword ptr [rbx + 0x18], 0
003DF350  mov      byte ptr [rbx + 0x10], 4
003DF354  add      rsp, 0x30
003DF358  pop      rbx
003DF359  ret      
```
