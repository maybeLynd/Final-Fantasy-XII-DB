# F homing pack: `00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0034AC30 (54 B, extent 0034AC30-0034AC66)

Documented callee on this page: `00379F20`

```
0034AC30  mov      qword ptr [rsp + 8], rbx
0034AC35  push     rdi
0034AC36  sub      rsp, 0x20
0034AC3A  mov      rcx, r9
0034AC3D  mov      rbx, rdx
0034AC40  call     0x267e10  ; -> 00267E10 fn
0034AC45  movzx    ecx, byte ptr [rbx + 0x15]
0034AC49  mov      edi, eax
0034AC4B  call     0x267310  ; -> 00267310 fn
0034AC50  test     eax, eax
0034AC52  jne      0x34ac5b  ; -> 0034AC5B
0034AC54  mov      ecx, edi
0034AC56  call     0x379f20  ; -> 00379F20 fn
0034AC5B  mov      rbx, qword ptr [rsp + 0x30]
0034AC60  add      rsp, 0x20
0034AC64  pop      rdi
0034AC65  ret      
```
