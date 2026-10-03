# F homing pack (FABLE): `16-UI/Message-Windows/the-message-window-layout-readers.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 002E22A0 (71 B, extent 002E22A0-002E22E7)

Documented callee on this page: `002A30B0`

```
002E22A0  mov      r8d, edx
002E22A3  mov      eax, 7
002E22A8  test     ecx, ecx
002E22AA  jns      0x2e22da  ; -> 002E22DA
002E22AC  xor      ecx, ecx
002E22AE  cmp      ecx, eax
002E22B0  cmovg    ecx, eax
002E22B3  movsxd   rax, ecx
002E22B6  imul     rdx, rax, 0x68
002E22BA  lea      rax, [rip + 0x1e7cf3f]  ; -> 0215F200
002E22C1  mov      rcx, qword ptr [rdx + rax]
002E22C5  test     rcx, rcx
002E22C8  je       0x2e22d9  ; -> 002E22D9
002E22CA  cmp      byte ptr [rdx + rax + 0x3c], 0xff
002E22CF  je       0x2e22d9  ; -> 002E22D9
002E22D1  mov      edx, r8d
002E22D4  jmp      0x2a30b0  ; -> 002A30B0 fn
002E22D9  ret      
002E22DA  cmp      ecx, eax
002E22DC  cmovg    ecx, eax
002E22DF  test     ecx, ecx
002E22E1  jns      0x2e22ae  ; -> 002E22AE
002E22E3  xor      ecx, ecx
002E22E5  jmp      0x2e22b3  ; -> 002E22B3
```
