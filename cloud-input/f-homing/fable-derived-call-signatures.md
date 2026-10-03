# F homing pack (FABLE): `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00511660 (61 B, extent 00511660-0051169D)

Documented callee on this page: `002D6640`

```
00511660  push     rdi
00511662  sub      rsp, 0x20
00511666  mov      rdi, r9
00511669  call     0x280120  ; -> 00280120 fn
0051166E  test     eax, eax
00511670  jne      0x511697  ; -> 00511697
00511672  mov      rcx, rdi
00511675  mov      qword ptr [rsp + 0x30], rbx
0051167A  call     0x267e10  ; -> 00267E10 fn
0051167F  mov      rcx, rdi
00511682  mov      ebx, eax
00511684  call     0x267e10  ; -> 00267E10 fn
00511689  mov      edx, ebx
0051168B  mov      ecx, eax
0051168D  call     0x2d6640  ; -> 002D6640 fn
00511692  mov      rbx, qword ptr [rsp + 0x30]
00511697  add      rsp, 0x20
0051169B  pop      rdi
0051169C  ret      
```
