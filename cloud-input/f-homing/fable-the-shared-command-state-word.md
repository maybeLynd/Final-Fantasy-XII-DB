# F homing pack (FABLE): `17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0035E760 (41 B, extent 0035E760-0035E789)

Documented callee on this page: `00369160`

```
0035E760  sub      rsp, 0x28
0035E764  mov      eax, dword ptr [rip + 0x1f6be8e]  ; -> 022CA5F8
0035E76A  test     eax, eax
0035E76C  je       0x35e784  ; -> 0035E784
0035E76E  call     0x369160  ; -> 00369160 fn
0035E773  cmp      qword ptr [rax], 0
0035E777  je       0x35e784  ; -> 0035E784
0035E779  xor      ecx, ecx
0035E77B  add      rsp, 0x28
0035E77F  jmp      0x3691b0  ; -> 003691B0 fn
0035E784  add      rsp, 0x28
0035E788  ret      
```
