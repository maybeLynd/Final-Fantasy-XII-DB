# F homing pack (FABLE): `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00254FE0 (52 B, extent 00254FE0-00255014)

Documented callee on this page: `002E0FA0`

```
00254FE0  push     rbx
00254FE2  sub      rsp, 0x20
00254FE6  mov      ebx, dword ptr [rip + 0x1bb72bc]  ; -> 01E0C2A8 [u32 0x00000001]
00254FEC  xor      ebx, 1
00254FEF  mov      dword ptr [rip + 0x1bb72b3], ebx  ; -> 01E0C2A8 [u32 0x00000001]
00254FF5  call     0x2e0fa0  ; -> 002E0FA0 fn
00254FFA  bt       eax, 0xa
00254FFE  mov      eax, 0
00255003  cmovb    ebx, eax
00255006  xor      ecx, ecx
00255008  mov      edx, ebx
0025500A  add      rsp, 0x20
0025500E  pop      rbx
0025500F  jmp      0x28ffe0  ; -> 0028FFE0 fn
```

## 0028E580 (103 B, extent 0028E580-0028E5E7)

Documented callee on this page: `002E0FA0`

```
0028E580  mov      qword ptr [rsp + 8], rbx
0028E585  push     rdi
0028E586  sub      rsp, 0x20
0028E58A  call     0x35d5c0  ; -> 0035D5C0 fn
0028E58F  call     0x35c6f0  ; -> 0035C6F0 fn
0028E594  xor      ebx, ebx
0028E596  test     al, 2
0028E598  je       0x28e5a8  ; -> 0028E5A8
0028E59A  call     0x2e0fa0  ; -> 002E0FA0 fn
0028E59F  lea      ecx, [rbx + 1]
0028E5A2  bt       eax, 0xa
0028E5A6  jae      0x28e5aa  ; -> 0028E5AA
0028E5A8  mov      ecx, ebx
0028E5AA  call     0x366960  ; -> 00366960 fn
0028E5AF  call     0x366950  ; -> 00366950 fn
0028E5B4  mov      rdi, rbx
0028E5B7  nop      word ptr [rax + rax]
0028E5C0  mov      rcx, qword ptr [rip + 0x1e0d8b9]  ; -> 0209BE80
0028E5C7  mov      edx, ebx
0028E5C9  add      rcx, rdi
0028E5CC  call     0x296540  ; -> 00296540 fn
0028E5D1  inc      ebx
0028E5D3  add      rdi, 0x20
0028E5D7  cmp      ebx, 4
0028E5DA  jl       0x28e5c0  ; -> 0028E5C0
0028E5DC  mov      rbx, qword ptr [rsp + 0x30]
0028E5E1  add      rsp, 0x20
0028E5E5  pop      rdi
0028E5E6  ret      
```
