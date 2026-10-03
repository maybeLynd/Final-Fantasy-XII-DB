# F homing pack: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00347470 (49 B, extent 00347470-003474A1)

Documented callee on this page: `003DEC90`

```
00347470  mov      qword ptr [rsp + 8], rbx
00347475  push     rdi
00347476  sub      rsp, 0x20
0034747A  mov      rdi, r9
0034747D  call     0x2640c0  ; -> 002640C0 fn
00347482  mov      rcx, rdi
00347485  mov      rbx, rax
00347488  call     0x267e10  ; -> 00267E10 fn
0034748D  mov      ecx, dword ptr [rbx + 0x28]
00347490  mov      edx, eax
00347492  mov      rbx, qword ptr [rsp + 0x30]
00347497  add      rsp, 0x20
0034749B  pop      rdi
0034749C  jmp      0x3dec90  ; -> 003DEC90 fn
```
