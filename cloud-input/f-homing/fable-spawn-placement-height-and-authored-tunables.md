# F homing pack (FABLE): `05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00235DD0 (167 B, extent 00235DD0-00235E77)

Documented callee on this page: `0031A930`

```
00235DD0  sub      rsp, 0x68
00235DD4  movaps   xmmword ptr [rsp + 0x50], xmm6
00235DD9  movaps   xmmword ptr [rsp + 0x40], xmm7
00235DDE  mov      rax, qword ptr [rip + 0x1d0ea4b]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00235DE5  xor      rax, rsp
00235DE8  mov      qword ptr [rsp + 0x30], rax
00235DED  movaps   xmm7, xmm2
00235DF0  movaps   xmm6, xmm1
00235DF3  test     ecx, ecx
00235DF5  jns      0x235dfe  ; -> 00235DFE
00235DF7  call     0x3272a0  ; -> 003272A0 fn
00235DFC  jmp      0x235e03  ; -> 00235E03
00235DFE  call     0x31b810  ; -> 0031B810 fn
00235E03  test     rax, rax
00235E06  jne      0x235e12  ; -> 00235E12
00235E08  movss    xmm0, dword ptr [rip + 0x1ab5e8c]  ; -> 01CEBC9C [f32 -1]
00235E10  jmp      0x235e5b  ; -> 00235E5B
00235E12  xorps    xmm0, xmm0
00235E15  movss    dword ptr [rsp + 0x20], xmm6
00235E1B  movss    dword ptr [rsp + 0x24], xmm0
00235E21  lea      rcx, [rax + 0xe0]
00235E28  movss    dword ptr [rsp + 0x28], xmm7
00235E2E  lea      rdx, [rsp + 0x20]
00235E33  movss    xmm6, dword ptr [rax + 0x160]
00235E3B  movaps   xmm2, xmm6
00235E3E  call     0x31ac90  ; -> 0031AC90 fn
00235E43  movaps   xmm1, xmm6
00235E46  call     0x31a930  ; -> 0031A930 fn
00235E4B  mulss    xmm0, dword ptr [rip + 0x6cc5e5]  ; -> 00902438 [f32 360]
00235E53  divss    xmm0, dword ptr [rip + 0x1ab5e1d]  ; -> 01CEBC78 [f32 6.283185]
00235E5B  mov      rcx, qword ptr [rsp + 0x30]
00235E60  xor      rcx, rsp
00235E63  call     0x808c40  ; -> 00808C40 fn
00235E68  movaps   xmm6, xmmword ptr [rsp + 0x50]
00235E6D  movaps   xmm7, xmmword ptr [rsp + 0x40]
00235E72  add      rsp, 0x68
00235E76  ret      
```
