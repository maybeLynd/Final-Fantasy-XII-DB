# F homing pack (FABLE): `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 001EC000 (81 B, extent 001EC000-001EC051)

Documented callee on this page: `001EB800`

```
001EC000  cmp      qword ptr [rcx + 0x20], 0
001EC005  lea      rdx, [rcx + 0x20]
001EC009  je       0x1ec050  ; -> 001EC050
001EC00B  cmp      byte ptr [rcx + 0x26e], 0
001EC012  jne      0x1ec04b  ; -> 001EC04B
001EC014  inc      dword ptr [rdx + 8]
001EC017  mov      eax, dword ptr [rdx + 8]
001EC01A  cmp      eax, dword ptr [rdx + 0x10]
001EC01D  jge      0x1ec033  ; -> 001EC033
001EC01F  movss    xmm0, dword ptr [rdx + 0x18]
001EC024  addss    xmm0, dword ptr [rdx + 0x14]
001EC029  movss    dword ptr [rdx + 0x14], xmm0
001EC02E  jmp      0x1eb800  ; -> 001EB800 fn
001EC033  xorps    xmm0, xmm0
001EC036  xor      eax, eax
001EC038  comiss   xmm0, dword ptr [rdx + 0x14]
001EC03C  jbe      0x1ec041  ; -> 001EC041
001EC03E  mov      dword ptr [rdx + 0x14], eax
001EC041  mov      dword ptr [rdx + 0x10], 0xffffffff
001EC048  mov      qword ptr [rdx], rax
001EC04B  jmp      0x1eb800  ; -> 001EB800 fn
001EC050  ret      
```
