# F homing pack (FABLE): `13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 00300490 (28 B, extent 00300490-003004AC)

Documented callee on this page: `003008A0`

```
00300490  sub      rsp, 0x38
00300494  mov      dword ptr [rsp + 0x20], r8d
00300499  mov      r9d, 4
0030049F  xor      r8d, r8d
003004A2  call     0x3008a0  ; -> 003008A0 fn
003004A7  add      rsp, 0x38
003004AB  ret      
```

## 0030DD70 (78 B, extent 0030DD70-0030DDBE)

Documented callee on this page: `003008A0`

```
0030DD70  mov      qword ptr [rsp + 8], rbx
0030DD75  push     rdi
0030DD76  sub      rsp, 0x30
0030DD7A  xor      edi, edi
0030DD7C  mov      ebx, edi
0030DD7E  cmp      dword ptr [rip + 0x1bddf78], ebx  ; -> 01EEBCFC [u32 0x00000040]
0030DD84  jle      0x30ddb3  ; -> 0030DDB3
0030DD86  nop      word ptr [rax + rax]
0030DD90  mov      r9d, 1
0030DD96  mov      dword ptr [rsp + 0x20], edi
0030DD9A  xor      r8d, r8d
0030DD9D  movzx    ecx, bx
0030DDA0  lea      edx, [r9 + 0x62]
0030DDA4  call     0x3008a0  ; -> 003008A0 fn
0030DDA9  inc      ebx
0030DDAB  cmp      ebx, dword ptr [rip + 0x1bddf4b]  ; -> 01EEBCFC [u32 0x00000040]
0030DDB1  jl       0x30dd90  ; -> 0030DD90
0030DDB3  mov      rbx, qword ptr [rsp + 0x40]
0030DDB8  add      rsp, 0x30
0030DDBC  pop      rdi
0030DDBD  ret      
```

## 0032A810 (24 B, extent 0032A810-0032A828)

Documented callee on this page: `00300B80`

```
0032A810  sub      rsp, 0x28
0032A814  xor      r8d, r8d
0032A817  call     0x300b80  ; -> 00300B80 fn
0032A81C  xor      ecx, ecx
0032A81E  test     eax, eax
0032A820  cmovs    eax, ecx
0032A823  add      rsp, 0x28
0032A827  ret      
```
