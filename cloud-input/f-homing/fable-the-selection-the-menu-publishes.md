# F homing pack (FABLE): `16-UI/the-selection-the-menu-publishes.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0028C9F0 (62 B, extent 0028C9F0-0028CA2E)

Documented callee on this page: `00275490`

```
0028C9F0  mov      qword ptr [rsp + 8], rbx
0028C9F5  push     rdi
0028C9F6  sub      rsp, 0x20
0028C9FA  movss    xmm0, dword ptr [rdx + 0x20]
0028C9FF  mov      rbx, rdx
0028CA02  mulss    xmm0, dword ptr [rip + 0x639566]  ; -> 008C5F70 [f32 1.570796]
0028CA0A  mov      rdi, rcx
0028CA0D  call     0x861f0e  ; -> 00861F0E fn
0028CA12  movaps   xmm3, xmm0
0028CA15  lea      r8, [rbx + 0x10]
0028CA19  mov      rdx, rbx
0028CA1C  mov      rcx, rdi
0028CA1F  mov      rbx, qword ptr [rsp + 0x30]
0028CA24  add      rsp, 0x20
0028CA28  pop      rdi
0028CA29  jmp      0x275490  ; -> 00275490 fn
```
