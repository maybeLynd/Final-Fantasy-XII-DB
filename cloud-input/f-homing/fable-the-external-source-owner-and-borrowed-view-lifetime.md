# F homing pack (FABLE): `02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0026BA00 (87 B, extent 0026BA00-0026BA57)

Documented callee on this page: `00268380`

```
0026BA00  movzx    edx, byte ptr [rcx + 3]
0026BA04  mov      r8, rcx
0026BA07  shr      edx, 5
0026BA0A  sub      edx, 1
0026BA0D  je       0x26ba37  ; -> 0026BA37
0026BA0F  cmp      edx, 2
0026BA12  jne      0x26ba4f  ; -> 0026BA4F
0026BA14  mov      rdx, qword ptr [rcx + 0xb8]
0026BA1B  xorps    xmm0, xmm0
0026BA1E  comiss   xmm0, xmm1
0026BA21  movss    dword ptr [rdx + 0xc8], xmm1
0026BA29  seta     al
0026BA2C  mov      byte ptr [rdx + 0xdd], al
0026BA32  jmp      0x268380  ; -> 00268380 fn
0026BA37  mov      rcx, qword ptr [rcx + 0xb8]
0026BA3E  xorps    xmm0, xmm0
0026BA41  comiss   xmm0, xmm1
0026BA44  movss    dword ptr [rcx + 0x68], xmm1
0026BA49  seta     al
0026BA4C  mov      byte ptr [rcx + 0x5c], al
0026BA4F  mov      rcx, r8
0026BA52  jmp      0x268380  ; -> 00268380 fn
```
