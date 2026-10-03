# F homing pack (FABLE): `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 001F2F70 (31 B, extent 001F2F70-001F2F8F)

Documented callee on this page: `00186410`

```
001F2F70  push     rbx
001F2F72  sub      rsp, 0x20
001F2F76  mov      rbx, rcx
001F2F79  call     0x189120  ; -> 00189120 fn
001F2F7E  movzx    edx, byte ptr [rbx + 0x18]
001F2F82  mov      rcx, rax
001F2F85  add      rsp, 0x20
001F2F89  pop      rbx
001F2F8A  jmp      0x186410  ; -> 00186410 fn
```
