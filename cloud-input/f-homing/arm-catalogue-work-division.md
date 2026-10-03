# F homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md`

Generated 2026-10-02 22:29 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0065FC20 (95 B, extent 0065FC20-0065FC7F)

Documented callee on this page: `006737F0`

```
0065FC20  push     rbx
0065FC22  sub      rsp, 0x30
0065FC26  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0065FC2F  mov      rbx, rdx
0065FC32  mov      rcx, rdx
0065FC35  call     0x6737f0  ; -> 006737F0 fn
0065FC3A  test     byte ptr [rbx + 0x6c], 1
0065FC3E  je       0x65fc49  ; -> 0065FC49
0065FC40  mov      rcx, rbx
0065FC43  call     0x674420  ; -> 00674420 fn
0065FC48  nop      
0065FC49  mov      ecx, dword ptr [rbx + 0x18]
0065FC4C  mov      eax, ecx
0065FC4E  shr      eax, 0x1f
0065FC51  not      al
0065FC53  test     al, 1
0065FC55  je       0x65fc6e  ; -> 0065FC6E
0065FC57  btr      ecx, 0x1f
0065FC5B  cmp      ecx, 1
0065FC5E  jbe      0x65fc6e  ; -> 0065FC6E
0065FC60  mov      rcx, qword ptr [rbx + 0x20]
0065FC64  test     rcx, rcx
0065FC67  je       0x65fc6e  ; -> 0065FC6E
0065FC69  call     0x584730  ; -> 00584730 fn
0065FC6E  xor      eax, eax
0065FC70  mov      qword ptr [rbx + 0x20], rax
0065FC74  mov      dword ptr [rbx + 0x18], eax
0065FC77  mov      al, 1
0065FC79  add      rsp, 0x30
0065FC7D  pop      rbx
0065FC7E  ret      
```
