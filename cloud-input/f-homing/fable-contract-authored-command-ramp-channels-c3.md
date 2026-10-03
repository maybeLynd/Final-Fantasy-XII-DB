# F homing pack (FABLE): `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0042DFC0 (83 B, extent 0042DFC0-0042E013)

Documented callee on this page: `00422EB0`

```
0042DFC0  mov      qword ptr [rsp + 8], rbx
0042DFC5  push     rdi
0042DFC6  sub      rsp, 0x20
0042DFCA  xor      eax, eax
0042DFCC  mov      rdi, rdx
0042DFCF  cmp      word ptr [rcx + 6], -1
0042DFD4  mov      rbx, rcx
0042DFD7  je       0x42dff9  ; -> 0042DFF9
0042DFD9  cmp      word ptr [rcx + 0x2f2], 1
0042DFE1  je       0x42dff9  ; -> 0042DFF9
0042DFE3  cmp      word ptr [rcx + 0x2f8], -1
0042DFEB  jne      0x42dff9  ; -> 0042DFF9
0042DFED  test     dword ptr [rcx + 0x284], 0x8000000
0042DFF7  je       0x42dffe  ; -> 0042DFFE
0042DFF9  call     0x422eb0  ; -> 00422EB0 fn
0042DFFE  cmp      word ptr [rbx + 6], -1
0042E003  jne      0x42e008  ; -> 0042E008
0042E005  mov      dword ptr [rdi + 0x58], eax
0042E008  mov      rbx, qword ptr [rsp + 0x30]
0042E00D  add      rsp, 0x20
0042E011  pop      rdi
0042E012  ret      
```
