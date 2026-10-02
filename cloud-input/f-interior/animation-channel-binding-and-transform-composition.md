# F-interior pack: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/animation-channel-binding-and-transform-composition.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 959a77e13	SWE2-DATA: DD owner read batch 2 - six Middleware and CRT pages reconciled, residue registered as SD; 65f4854dd	SWE2-STRUCT pass-22 debt + OV31 narrowing: 77 crossing bullets across 21 docs (5 lane folders now re; inbox mentions: repos-c9.md, xiionline-8d.md). OPUS read these before packing.

## 0063BB60 (58 B, extent 0063BB60-0063BB9A)

Page context: "ery argument, so the second call returns exactly what the first did.       - **Not members.** The 'PClassDataMemberDynamicType<…>' adaptors use different slot-1 bodies that take an argument         ('0063BB60', '00677A80'), and their interface's slot 1 is '_purecall'. They are type adaptors, not entries of a class's         member list. This census does not show that one can never appear where '005C0820' looks. - [x] ~~**UQ-281.** What "

```
0063BB60  push     rbx
0063BB62  sub      rsp, 0x20
0063BB66  mov      r8, qword ptr [rcx + 0x10]
0063BB6A  mov      rbx, rcx
0063BB6D  test     r8, r8
0063BB70  je       0x63bb8c  ; -> 0063BB8C
0063BB72  movsxd   rax, dword ptr [rcx + 0x18]
0063BB76  lea      rcx, [rdx - 8]
0063BB7A  add      rcx, rax
0063BB7D  test     rdx, rdx
0063BB80  cmove    rcx, rax
0063BB84  call     r8
0063BB87  test     rax, rax
0063BB8A  jne      0x63bb94  ; -> 0063BB94
0063BB8C  mov      rax, qword ptr [rbx + 8]
0063BB90  mov      rax, qword ptr [rax + 0x30]
0063BB94  add      rsp, 0x20
0063BB98  pop      rbx
0063BB99  ret      
```

## 00677A80 (46 B, extent 00677A80-00677AAE)

Page context: ", so the second call returns exactly what the first did.       - **Not members.** The 'PClassDataMemberDynamicType<…>' adaptors use different slot-1 bodies that take an argument         ('0063BB60', '00677A80'), and their interface's slot 1 is '_purecall'. They are type adaptors, not entries of a class's         member list. This census does not show that one can never appear where '005C0820' looks. - [x] ~~**UQ-281.** What member type "

```
00677A80  push     rbx
00677A82  sub      rsp, 0x20
00677A86  mov      rax, qword ptr [rcx + 0x10]
00677A8A  mov      rbx, rcx
00677A8D  test     rax, rax
00677A90  je       0x677aa0  ; -> 00677AA0
00677A92  movsxd   rcx, dword ptr [rcx + 0x18]
00677A96  add      rcx, rdx
00677A99  call     rax
00677A9B  test     rax, rax
00677A9E  jne      0x677aa8  ; -> 00677AA8
00677AA0  mov      rax, qword ptr [rbx + 8]
00677AA4  mov      rax, qword ptr [rax + 0x30]
00677AA8  add      rsp, 0x20
00677AAC  pop      rbx
00677AAD  ret      
```
