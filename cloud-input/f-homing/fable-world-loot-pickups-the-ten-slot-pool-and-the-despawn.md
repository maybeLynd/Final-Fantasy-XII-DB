# F homing pack (FABLE): `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003B7440 (202 B, extent 003B7440-003B750A)

Documented callee on this page: `003B73B0`

```
003B7440  push     rsi
003B7442  sub      rsp, 0x20
003B7446  mov      rcx, qword ptr [rip + 0x2b0581b]  ; -> 02EBCC68
003B744D  call     0x3b73b0  ; -> 003B73B0 fn
003B7452  xor      esi, esi
003B7454  cmp      dword ptr [rip + 0x2b05806], esi  ; -> 02EBCC60
003B745A  jle      0x3b7504  ; -> 003B7504
003B7460  mov      qword ptr [rsp + 0x30], rbx
003B7465  mov      qword ptr [rsp + 0x40], r14
003B746A  lea      r14, [rip + 0x2b0564f]  ; -> 02EBCAC0
003B7471  mov      qword ptr [rsp + 0x38], rdi
003B7476  mov      rbx, qword ptr [r14]
003B7479  test     rbx, rbx
003B747C  je       0x3b74e7  ; -> 003B74E7
003B747E  mov      rcx, rbx
003B7481  call     0x359b80  ; -> 00359B80 fn
003B7486  mov      rdi, rax
003B7489  test     rax, rax
003B748C  je       0x3b74e7  ; -> 003B74E7
003B748E  lea      r9, [rax + 8]
003B7492  mov      rdx, rax
003B7495  lea      r8, [rax + 4]
003B7499  mov      rcx, rbx
003B749C  call     0x265020  ; -> 00265020 fn
003B74A1  lea      r9, [rdi + 0x18]
003B74A5  mov      rcx, rbx
003B74A8  lea      r8, [rdi + 0x14]
003B74AC  lea      rdx, [rdi + 0x10]
003B74B0  call     0x265240  ; -> 00265240 fn
003B74B5  mov      rcx, rbx
003B74B8  call     0x2e9be0  ; -> 002E9BE0 fn
003B74BD  mov      rcx, rbx
003B74C0  mov      byte ptr [rdi + 0x64], al
003B74C3  call     0x263cc0  ; -> 00263CC0 fn
003B74C8  mov      rcx, rbx
003B74CB  movss    dword ptr [rdi + 0x34], xmm0
003B74D0  call     0x265200  ; -> 00265200 fn
003B74D5  mov      rcx, rbx
003B74D8  movss    dword ptr [rdi + 0x24], xmm0
003B74DD  call     0x263cc0  ; -> 00263CC0 fn
003B74E2  movss    dword ptr [rdi + 0x34], xmm0
003B74E7  inc      esi
003B74E9  add      r14, 8
003B74ED  cmp      esi, dword ptr [rip + 0x2b0576d]  ; -> 02EBCC60
003B74F3  jl       0x3b7476  ; -> 003B7476
003B74F5  mov      r14, qword ptr [rsp + 0x40]
003B74FA  mov      rdi, qword ptr [rsp + 0x38]
003B74FF  mov      rbx, qword ptr [rsp + 0x30]
003B7504  add      rsp, 0x20
003B7508  pop      rsi
003B7509  ret      
```
