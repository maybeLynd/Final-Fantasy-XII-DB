# F homing pack (FABLE): `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 0028E070 (77 B, extent 0028E070-0028E0BD)

Documented callee on this page: `002BDB60`

```
0028E070  sub      rsp, 0x28
0028E074  mov      rax, qword ptr [rip + 0x1e0de05]  ; -> 0209BE80
0028E07B  test     rax, rax
0028E07E  je       0x28e0b8  ; -> 0028E0B8
0028E080  or       dword ptr [rax + 0x10f68], 0x40
0028E087  mov      rcx, qword ptr [rip + 0x1e0ddf2]  ; -> 0209BE80
0028E08E  add      rcx, 0x8fa0
0028E095  call     0x2bdb60  ; -> 002BDB60 fn
0028E09A  mov      rcx, qword ptr [rip + 0x1e0dddf]  ; -> 0209BE80
0028E0A1  test     rcx, rcx
0028E0A4  je       0x28e0b8  ; -> 0028E0B8
0028E0A6  add      rcx, 0x8fa0
0028E0AD  xor      edx, edx
0028E0AF  add      rsp, 0x28
0028E0B3  jmp      0x2bdca0  ; -> 002BDCA0 fn
0028E0B8  add      rsp, 0x28
0028E0BC  ret      
```

## 0028E0C0 (80 B, extent 0028E0C0-0028E110)

Documented callee on this page: `002BDC00`

```
0028E0C0  sub      rsp, 0x28
0028E0C4  mov      rax, qword ptr [rip + 0x1e0ddb5]  ; -> 0209BE80
0028E0CB  test     rax, rax
0028E0CE  je       0x28e10b  ; -> 0028E10B
0028E0D0  and      dword ptr [rax + 0x10f68], 0xffffffbf
0028E0D7  mov      rcx, qword ptr [rip + 0x1e0dda2]  ; -> 0209BE80
0028E0DE  add      rcx, 0x8fa0
0028E0E5  call     0x2bdc00  ; -> 002BDC00 fn
0028E0EA  mov      rcx, qword ptr [rip + 0x1e0dd8f]  ; -> 0209BE80
0028E0F1  test     rcx, rcx
0028E0F4  je       0x28e10b  ; -> 0028E10B
0028E0F6  add      rcx, 0x8fa0
0028E0FD  mov      edx, 1
0028E102  add      rsp, 0x28
0028E106  jmp      0x2bdca0  ; -> 002BDCA0 fn
0028E10B  add      rsp, 0x28
0028E10F  ret      
```
