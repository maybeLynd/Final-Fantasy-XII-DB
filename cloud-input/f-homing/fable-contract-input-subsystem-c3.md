# F homing pack (FABLE): `15-Input/CONTRACT-input-subsystem.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00344410 (36 B, extent 00344410-00344434)

Documented callee on this page: `00342770`

```
00344410  push     rbx
00344412  sub      rsp, 0x20
00344416  mov      rbx, r8
00344419  call     0x342770  ; -> 00342770 fn
0034441E  and      byte ptr [rbx + 2], 0xf1
00344422  or       byte ptr [rbx + 2], 1
00344426  and      byte ptr [rbx + 3], 0xbf
0034442A  add      rsp, 0x20
0034442E  pop      rbx
0034442F  jmp      0x25d5d0  ; -> 0025D5D0 fn
```
